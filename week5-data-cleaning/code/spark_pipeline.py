from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import DoubleType, IntegerType

# Initialize Spark Session
spark = (
    SparkSession.builder
    .appName("Week5_Data_Cleaning")
    .master("local[*]")
    .getOrCreate()
)

spark.sparkContext.setLogLevel("ERROR")

print("=" * 60)
print("Loading Dataset")
print("=" * 60)

df = (
    spark.read
    .option("header", True)
    .option("inferSchema", False)
    .option("multiLine", True)
    .option("escape", '"')
    .option("quote", '"')
    .csv("./week5-data-cleaning/dataset/Superstore.csv")
)

print("Rows :", df.count())
df.printSchema()
df.show(5)

print("\nRemoving duplicate rows...")
before = df.count()
df = df.dropDuplicates()
after = df.count()
print("Duplicates Removed :", before - after)

print("\nRenaming Columns")
df = (
    df.withColumnRenamed("Order ID", "Order_ID")
    .withColumnRenamed("Ship Mode", "Ship_Mode")
    .withColumnRenamed("Customer ID", "Customer_ID")
    .withColumnRenamed("Customer Name", "Customer_Name")
    .withColumnRenamed("Postal Code", "Postal_Code")
    .withColumnRenamed("Product ID", "Product_ID")
    .withColumnRenamed("Sub-Category", "Sub_Category")
)

print("\nCasting Columns")
df = (
    df.withColumn("Sales", F.col("Sales").cast(DoubleType()))
    .withColumn("Quantity", F.col("Quantity").cast(IntegerType()))
    .withColumn("Discount", F.col("Discount").cast(DoubleType()))
    .withColumn("Profit", F.col("Profit").cast(DoubleType()))
)

print("\nChecking Null Values")
nulls = df.select([
    F.count(F.when(F.col(c).isNull(), c)).alias(c) for c in df.columns
])
nulls.show(truncate=False)

print("Replacing null values...")
df = df.fillna({
    "Category": "Unknown",
    "Sub_Category": "Unknown",
    "Region": "Unknown",
    "Sales": 0.0,
    "Profit": 0.0,
    "Quantity": 0
})

print("=" * 60)
print("Filtering Data")
print("=" * 60)

cleanDf = df.filter(
    (F.col("Region") != "Unknown") &
    (F.col("Category") != "Unknown") &
    (F.col("Sales") > 100)
)

print("Filtered Rows :", cleanDf.count())
cleanDf.show(10)

print("=" * 60)
print("Overall Aggregation")
print("=" * 60)

cleanDf.select(
    F.count("*").alias("Total Orders"),
    F.sum("Sales").alias("Total Sales"),
    F.avg("Sales").alias("Average Sales"),
    F.min("Sales").alias("Minimum Sales"),
    F.max("Sales").alias("Maximum Sales")
).show()

print("=" * 60)
print("Sales by Category")
print("=" * 60)

catDf = (
    cleanDf.groupBy("Category").agg(
        F.count("*").alias("Orders"),
        F.sum("Sales").alias("TotalSales"),
        F.avg("Profit").alias("AverageProfit"),
        F.max("Sales").alias("HighestSale"),
        F.min("Sales").alias("LowestSale")
    )
    .orderBy(F.desc("TotalSales"))
)

catDf.show()

print("=" * 60)
print("Sales by Region")
print("=" * 60)

regionDf = (
    cleanDf.groupBy("Region").agg(
        F.count("*").alias("Orders"),
        F.sum("Sales").alias("Revenue"),
        F.avg("Profit").alias("AverageProfit")
    )
    .orderBy(F.desc("Revenue"))
)

regionDf.show()

print("=" * 60)
print("Category + Region")
print("=" * 60)

summaryDf = cleanDf.groupBy("Category", "Region").agg(
    F.count("*").alias("Orders"),
    F.sum("Sales").alias("Revenue"),
    F.avg("Profit").alias("AverageProfit")
)

summaryDf.show()

print("\nGroups having more than 10 orders")
summaryDf.filter(F.col("Orders") > 10).show()

print("\nExecution Plan (Shuffle after groupBy)")
summaryDf.explain()

print("=" * 60)
print("Adding Profit Status Column")
print("=" * 60)

finalDf = cleanDf.withColumn(
    "Profit_Status",
    F.when(F.col("Profit") > 0, "Profit").otherwise("Loss")
)

finalDf.show(10)

print("=" * 60)
print("Profit Status Summary")
print("=" * 60)

finalDf.groupBy("Profit_Status").agg(
    F.count("*").alias("Orders"),
    F.sum("Sales").alias("Sales")
).show()

print("=" * 60)
print("Saving Output")
print("=" * 60)

(
    finalDf.coalesce(1)
    .write.mode("overwrite")
    .option("header", True)
    .csv("./week5-data-cleaning/output/cleaned_data")
)

(
    summaryDf.coalesce(1)
    .write.mode("overwrite")
    .option("header", True)
    .csv("./week5-data-cleaning/output/category_region_summary")
)

(
    catDf.coalesce(1)
    .write.mode("overwrite")
    .option("header", True)
    .csv("./week5-data-cleaning/output/category_summary")
)

(
    regionDf.coalesce(1)
    .write.mode("overwrite")
    .option("header", True)
    .csv("./week5-data-cleaning/output/region_summary")
)

print("Done!")

spark.stop()