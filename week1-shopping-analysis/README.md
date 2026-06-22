# Shopping Dataset Analysis using Pandas

## Overview

This project focuses on learning the fundamentals of data exploration and data cleaning using the Pandas library in Python. A shopping dataset was used to practice common data preprocessing tasks such as handling missing values, removing duplicates, filtering records, and creating derived features.

The goal of the project is to understand how raw data can be transformed into a cleaner and more useful format before performing further analysis.

---

## Dataset

The dataset used in this project contains information about various shopping products, including:

* Product details
* Ratings and review counts
* Prices and discounts
* Seller information
* Product categories

### Files

* `shopping_dataset.csv` – Original dataset
* `cleaned_shopping_dataset.csv` – Cleaned dataset generated after preprocessing

---

## Tasks Performed

### 1. Loading the Dataset

* Imported the required Python libraries.
* Loaded the CSV file into a Pandas DataFrame.

### 2. Data Exploration

* Viewed the first and last few records.
* Checked dataset dimensions.
* Examined column names and data types.
* Generated summary statistics.

### 3. Handling Missing Values

* Identified missing values in the dataset.
* Calculated missing value percentages.
* Filled missing values using appropriate strategies for numerical and categorical columns.

### 4. Basic Data Operations

* Selected relevant columns.
* Filtered products based on conditions.
* Sorted records by rating and price.

### 5. Removing Duplicate Records

* Detected duplicate entries.
* Removed duplicate rows to improve data quality.

### 6. Feature Engineering

* Created a new column called `discount_value` to calculate the actual discount amount for each product.

### 7. Exporting Cleaned Data

* Saved the processed dataset as a new CSV file.

---

## Technologies Used

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Jupyter Notebook

---

## Project Structure

```text
week1-shopping-analysis/
│
├── data/
│   ├── shopping_dataset.csv
│   └── cleaned_shopping_dataset.csv
│
├── notebook/
│   └── shopping_dataset_analysis.ipynb
│
├── README.md
│
└── requirements.txt
```

---

## Key Learnings

Through this project, I gained hands-on experience with:

* Reading and working with CSV files in Pandas
* Exploring datasets efficiently
* Cleaning and preprocessing real-world data
* Handling missing values and duplicates
* Creating derived features from existing columns
* Saving processed datasets for future analysis

---

## Conclusion

This project demonstrates the basic workflow of data cleaning and exploration using Pandas. The cleaned dataset is more structured and suitable for further analysis, visualization, or machine learning tasks.
