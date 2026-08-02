# Delta Lake MERGE Implementation Assignment

This repository contains my solution for the Delta Lake MERGE assignment on incremental data processing using **PySpark** and **Delta Lake** on the Superstore dataset.

The project is split into two modules:
1. **(Data Cleaning & Incremental Prep)**: Reads `superstore.csv`, extracts unique customer entities, handles null values, removes duplicates, and generates `customer_master.csv` and `customer_incremental.csv`.
2. **(Spark Delta MERGE Pipeline)**: Initializes PySpark with Delta Lake, loads master data, applies the MERGE operation to process incremental updates and inserts, validates row counts, checks transaction logs, and demonstrates Delta Time Travel.

---

## 📁 Repository Structure

```text
week7-databricks/
│
├── data/
│   ├── superstore.csv            # Original raw Superstore dataset
│   ├── customer_master.csv       # Baseline customer master data (100 base records)
│   └── customer_incremental.csv  # Incremental batch (10 updates + 5 new inserts)
│
├── notebooks/
│   ├── data_cleaning.ipynb         # File 1: Data Cleaning Notebook
│   └── spark_delta_pipeline.ipynb  # File 2: Spark Delta MERGE Pipeline Notebook
│
├── screenshots/
│   ├── data_loading
│   ├── data_cleaning
│   ├── scd1
│   ├── validation
│   └── final_output
│
└── README.md                          # Project documentation
```

---

## 📊 Summary of Incremental Record Changes

| Customer ID | Action | Details of Changes |
| :--- | :--- | :--- |
| **AA-10315** | Updated | City changed to New York, State to New York |
| **AA-10375** | Updated | City changed to Los Angeles, State to California |
| **AA-10480** | Updated | City changed to Chicago, State to Illinois |
| **AA-10645** | Updated | City changed to Houston, State to Texas |
| **AB-10015** | Updated | City changed to Phoenix, State to Arizona |
| **NEW-001** | Inserted | Alex Turner (Seattle, WA) |
| **NEW-002** | Inserted | Bianca Dev (Boston, MA) |
| **NEW-003** | Inserted | Charlie Hayes (Austin, TX) |
| **NEW-004** | Inserted | Diana Prince (Denver, CO) |
| **NEW-005** | Inserted | Ethan Hunt (Miami, FL) |