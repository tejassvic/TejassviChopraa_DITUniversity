import time
from pyspark.sql import SparkSession
from pyspark.sql.types import *
from pyspark.sql.functions import *

# --------------------------------------------------
# Create Spark Session
# --------------------------------------------------
spark = SparkSession.builder \
    .appName("Week6_Spark_Intro") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")

# --------------------------------------------------
# File Paths
# --------------------------------------------------
INPUT_FILE = "./week6-spark-intro/dataset/Superstore.csv"
CSV_OUTPUT = "./week6-spark-intro/output/superstore_csv"
PARQUET_OUTPUT = "./week6-spark-intro/output/superstore_parquet"

# --------------------------------------------------
# Define Schema
# --------------------------------------------------
schema = StructType([
    StructField("Row ID", IntegerType(), True),
    StructField("Order ID", StringType(), True),
    StructField("Order Date", StringType(), True),
    StructField("Ship Date", StringType(), True),
    StructField("Ship Mode", StringType(), True),
    StructField("Customer ID", StringType(), True),
    StructField("Customer Name", StringType(), True),
    StructField("Segment", StringType(), True),
    StructField("Country", StringType(), True),
    StructField("City", StringType(), True),
    StructField("State", StringType(), True),
    StructField("Postal Code", StringType(), True),
    StructField("Region", StringType(), True),
    StructField("Product ID", StringType(), True),
    StructField("Category", StringType(), True),
    StructField("Sub-Category", StringType(), True),
    StructField("Product Name", StringType(), True),
    StructField("Sales", DoubleType(), True),
    StructField("Quantity", IntegerType(), True),
    StructField("Discount", DoubleType(), True),
    StructField("Profit", DoubleType(), True)
])

# --------------------------------------------------
# Read CSV
# --------------------------------------------------
df = spark.read \
    .option("header", True) \
    .schema(schema) \
    .csv(INPUT_FILE)
print("\n========== Original Data ==========")
df.show(5)
print("\n========== Schema ==========")
df.printSchema()
print("\nTotal Rows :", df.count())

# --------------------------------------------------
# Handle Null Values
# --------------------------------------------------
print("\nRemoving rows with null Sales or Quantity...")
df = df.na.drop(subset=["Sales", "Quantity"])
df = df.na.fill({
    "City": "Unknown",
    "State": "Unknown"
})

# --------------------------------------------------
# Rename Columns
# --------------------------------------------------
df = df.withColumnRenamed("Order ID", "Order_ID") \
       .withColumnRenamed("Customer Name", "Customer_Name")

# --------------------------------------------------
# Cast Data Types
# --------------------------------------------------
df = df.withColumn("Sales", col("Sales").cast("double")) \
       .withColumn("Quantity", col("Quantity").cast("int")) \
       .withColumn("Profit", col("Profit").cast("double"))

# --------------------------------------------------
# Convert Date Columns
# --------------------------------------------------
df = df.withColumn("Order Date", to_date(col("Order Date"), "M/d/yyyy")) \
       .withColumn("Ship Date", to_date(col("Ship Date"), "M/d/yyyy"))

# --------------------------------------------------
# Select Required Columns
# --------------------------------------------------
selected_df = df.select(
    "Order_ID",
    "Customer_Name",
    "Category",
    "Region",
    "Sales",
    "Quantity",
    "Profit"
)
print("\n========== Selected Columns ==========")
selected_df.show(5)

# --------------------------------------------------
# Filter Data
# --------------------------------------------------
filtered_df = selected_df.filter(col("Sales") > 500)
print("\n========== Sales > 500 ==========")
filtered_df.show(5)

# --------------------------------------------------
# Add New Columns
# --------------------------------------------------
filtered_df = filtered_df.withColumn("GST", round(col("Sales") * 0.18, 2)) \
                         .withColumn("Discounted_Sales", round(col("Sales") * 0.90, 2)) \
                         .withColumn("Profit_Margin", round((col("Profit") / col("Sales")) * 100, 2))
print("\n========== New Columns ==========")
filtered_df.show(5)

# --------------------------------------------------
# Narrow Transformation
# --------------------------------------------------
print("\n========== Narrow Transformation ==========")
narrow_df = filtered_df.select("Category", "Sales", "GST")
narrow_df.show(5)

# --------------------------------------------------
# Wide Transformation (Shuffle)
# --------------------------------------------------
print("\n========== Sales by Category ==========")
category_sales = filtered_df.groupBy("Category").agg(
    round(sum("Sales"), 2).alias("Total_Sales"),
    round(avg("Profit"), 2).alias("Average_Profit")
)

category_sales.show()

# --------------------------------------------------
# Save CSV
# --------------------------------------------------
filtered_df.write \
    .mode("overwrite") \
    .option("header", True) \
    .csv(CSV_OUTPUT)

print("\nCSV Saved Successfully")

# --------------------------------------------------
# Save Parquet
# --------------------------------------------------
filtered_df.write \
    .mode("overwrite") \
    .parquet(PARQUET_OUTPUT)
print("Parquet Saved Successfully")

# --------------------------------------------------
# Read Parquet
# --------------------------------------------------
parquet_df = spark.read.parquet(PARQUET_OUTPUT)
print("\n========== Reading Parquet ==========")
parquet_df.show(5)

# --------------------------------------------------
# CSV vs Parquet Performance
# --------------------------------------------------
print("\n========== Performance Comparison ==========")
start = time.time()
spark.read \
    .option("header", True) \
    .schema(schema) \
    .csv(INPUT_FILE) \
    .count()
csv_time = time.time() - start
start = time.time()
spark.read.parquet(PARQUET_OUTPUT).count()
parquet_time = time.time() - start
print(f"CSV Read Time      : {csv_time:.4f} seconds")
print(f"Parquet Read Time  : {parquet_time:.4f} seconds")

# --------------------------------------------------
# Actions
# --------------------------------------------------
print("\n========== Actions ==========")
print("Total Records :", filtered_df.count())
filtered_df.show(10)
print("First Record")
print(filtered_df.first())

# --------------------------------------------------
# Stop Spark
# --------------------------------------------------
spark.stop()