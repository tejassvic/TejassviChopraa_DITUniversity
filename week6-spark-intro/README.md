# Spark ETL Pipeline using PySpark

## Overview

This project was completed to understand the basics of Apache Spark and perform data processing using PySpark. I used the **Sample Superstore** dataset to build a simple ETL pipeline where the data is read from a CSV file, transformed, filtered, and then saved in both CSV and Parquet formats.

The project also covers Spark concepts like Lazy Evaluation, schema handling, transformations, actions, and compares the read performance of CSV and Parquet files.

---

## Dataset

- **Dataset:** Sample Superstore
- **Total Records:** 9994

---

## Spark Architecture

Apache Spark mainly consists of three components:

- **Driver** – Starts the Spark application and creates the Spark Session.
- **Cluster Manager** – Allocates resources for the application.
- **Executors** – Execute tasks and process the data.

---

## Lazy Evaluation

Spark follows **Lazy Evaluation**, which means transformations such as `select()`, `filter()`, and `withColumn()` are not executed immediately. Spark waits until an action like `show()`, `count()`, or `write()` is called before processing the data. This helps avoid unnecessary work and improves execution.

---

## Data Processing Steps

The following operations were performed:

- Read the CSV file using an explicit schema
- Displayed the dataset schema
- Removed rows with null values in important columns
- Renamed columns
- Converted date and numeric columns to the correct data types
- Selected only the required columns
- Filtered records where **Sales > 500**
- Added three new columns:
  - GST
  - Discounted Sales
  - Profit Margin
- Performed category-wise aggregation using `groupBy()`
- Saved the processed data in CSV format
- Saved the processed data in Parquet format
- Read the Parquet file again to verify the output
- Compared the read time of CSV and Parquet files

---

## Output Summary

### Total Records

```text
9994
```

### Records After Filtering (Sales > 500)

```text
1151
```

### Category-wise Sales

| Category | Total Sales | Average Profit |
|----------|------------:|---------------:|
| Office Supplies | 371333.76 | 191.26 |
| Furniture | 490694.15 | 44.22 |
| Technology | 605739.59 | 276.81 |

---

## Performance Comparison

| File Format | Read Time |
|-------------|----------:|
| CSV | 0.1728 sec |
| Parquet | 0.1877 sec |

For this dataset, both formats showed similar performance. The CSV file was slightly faster in this run because the dataset is relatively small.

---

## Technologies Used

- Python
- PySpark
- Java

---


## Concepts Covered

- Spark Architecture
- Lazy Evaluation
- Schema Handling
- DataFrames
- Transformations
- Actions
- Narrow and Wide Transformations
- Shuffle (`groupBy`)
- CSV and Parquet File Formats
- ETL Pipeline

---

## Conclusion

In this project, I learned how to use PySpark to process data using DataFrames. I performed data cleaning, filtering, column transformations, and aggregation before saving the final output in CSV and Parquet formats. I also understood the difference between transformations and actions and built a simple ETL pipeline using Apache Spark.