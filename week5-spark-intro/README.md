# Spark Fundamentals – Data Cleaning, Transformation & Aggregation using PySpark

**Technology:** Apache Spark (PySpark)
**Dataset:** Sample - Superstore.csv (Kaggle)

---

## Project Overview

This project is part of my Week 5 assignment, where I learned the fundamentals of Apache Spark and performed data cleaning, transformation, filtering, and aggregation using Spark DataFrames.

The main objective of this assignment was to understand why Spark is faster than MapReduce, learn how Spark DataFrames work, and build a complete data processing pipeline using the Superstore dataset.

During this assignment, I loaded the dataset into Spark, cleaned the data, removed duplicates, handled null values, applied filters, performed different aggregation operations, grouped the data using multiple columns, and created a new derived column to analyze profit and loss.

---

## Dataset Used

For this assignment, I used the following dataset:

`Sample - Superstore.csv`

The dataset contains sales information from a retail store and includes details such as:

* Order ID
* Customer Name
* Product Name
* Category
* Region
* Sales
* Quantity
* Discount
* Profit

The dataset contains:

**Total Records:** `9,994`

---

## Task 1 – Loading the Dataset

The first step was to create a Spark Session and load the CSV file into a Spark DataFrame.

After loading the dataset, I verified the schema and displayed a few rows to ensure that the data was loaded correctly.

The dataset contained **21 columns** and **9,994 records**.

---

## Task 2 – Understanding Spark DataFrames

One of the objectives of this assignment was to understand Spark DataFrames.

Unlike traditional Python data structures, Spark DataFrames are immutable. This means that every transformation creates a new DataFrame instead of modifying the existing one.

During the assignment, I created multiple DataFrames after applying different operations such as filtering, renaming columns, handling null values, and grouping data.

---

## Task 3 – Data Cleaning

The next step was cleaning the dataset.

The following operations were performed:

* Removed duplicate records.
* Renamed columns to make them easier to use.
* Converted Sales, Quantity, Discount, and Profit columns into numeric data types.
* Checked every column for null values.
* Replaced missing values wherever required.

During duplicate checking, Spark reported:

```text
Duplicates Removed : 0
```

The null value check showed that the dataset did not contain missing values after processing.

---

## Task 4 – Filtering the Dataset

After cleaning the data, I applied filtering conditions.

The following filters were used:

* Region should not be Unknown.
* Category should not be Unknown.
* Sales greater than 100.

After applying these conditions, the remaining dataset contained:

```text
Filtered Rows : 3765
```

This reduced the dataset to only meaningful records for further analysis.

---

## Task 5 – Aggregation Operations

Spark provides several aggregation functions which were used in this assignment.

The following functions were applied:

* Count
* Sum
* Average
* Minimum
* Maximum

The overall result was:

| Metric        |        Value |
| ------------- | -----------: |
| Total Orders  |        3,765 |
| Total Sales   | 2,101,361.60 |
| Average Sales |       558.13 |
| Minimum Sales |       100.24 |
| Maximum Sales |    22,638.48 |

These aggregations helped summarize the complete dataset.

---

## Task 6 – Grouping Data

To understand sales performance, I grouped the dataset using different columns.

### Sales by Category

The dataset was grouped by **Category**.

| Category        | Orders | Total Sales |
| --------------- | -----: | ----------: |
| Technology      |  1,187 |  802,689.88 |
| Furniture       |  1,318 |  710,789.01 |
| Office Supplies |  1,260 |  587,882.71 |

From the results, Technology generated the highest total sales.

---

### Sales by Region

The dataset was also grouped by Region.

| Region  | Orders |    Revenue |
| ------- | -----: | ---------: |
| West    |  1,261 | 660,923.27 |
| East    |  1,064 | 621,789.30 |
| Central |    833 | 458,692.51 |
| South   |    607 | 359,956.52 |

The West region generated the highest revenue among all regions.

---

### Category and Region Analysis

I also grouped the data using both **Category** and **Region**.

This helped analyze sales performance across different regions for every product category.

After grouping, I applied a condition to display only groups having more than **10 orders**, which is similar to using a **HAVING** clause in SQL.

---

## Task 7 – Shuffle Operations

One important concept in Spark is the shuffle operation.

Whenever Spark performs a `groupBy()`, it redistributes data between partitions so that records with the same key are processed together.

To understand this process, I used:

```python
summaryDf.explain()
```

The execution plan clearly showed the **Exchange** operation, indicating that Spark performed a shuffle before completing the aggregation.

This helped me understand how Spark executes wide transformations internally.

---

## Task 8 – Creating a New Column

I created a new column called:

`Profit_Status`

The logic used was:

* Profit > 0 → Profit
* Profit ≤ 0 → Loss

This allowed me to classify every order based on whether it generated profit or loss.

The final summary was:

| Profit Status | Orders |        Sales |
| ------------- | -----: | -----------: |
| Profit        |  2,896 | 1,633,857.01 |
| Loss          |    869 |   467,504.59 |

---

## Task 9 – Complete Spark Pipeline

The complete Spark pipeline followed these steps:

```text
Load CSV
      |
      v
Print Schema
      |
      v
Remove Duplicates
      |
      v
Rename Columns
      |
      v
Cast Data Types
      |
      v
Check Null Values
      |
      v
Filter Data
      |
      v
Aggregation
      |
      v
Group By
      |
      v
Shuffle (Explain)
      |
      v
Create Profit Status
      |
      v
Display Results
```

This pipeline combines multiple Spark transformations and actions into a complete data processing workflow.

---

## What I Learned

While completing this assignment, I learned how to:

* Create a Spark Session.
* Load CSV files into Spark DataFrames.
* Understand DataFrame immutability.
* Rename and cast DataFrame columns.
* Remove duplicate records.
* Handle null values.
* Apply filtering conditions.
* Perform aggregation functions.
* Group data using one or more columns.
* Apply conditions on grouped data.
* Understand shuffle operations in Spark.
* Create new columns using Spark functions.
* Build a complete Spark data processing pipeline.

---

## Conclusion

This assignment gave me practical experience working with Apache Spark and PySpark.

I successfully loaded the Superstore dataset, cleaned and transformed the data, performed multiple filtering and aggregation operations, grouped records based on different categories and regions, and analyzed the overall sales performance.

I also learned how Spark executes wide transformations through shuffle operations and how DataFrames can be used to build scalable data processing pipelines.

Overall, this assignment helped me understand the basic workflow of Apache Spark and how it can efficiently process large datasets using DataFrames.
