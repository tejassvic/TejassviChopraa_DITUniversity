# RetailStream Inc. - Data Engineering Pipeline

## Project Overview
This repository contains the code and documentation for the RetailStream Inc. data pipeline project, completed as part of my data engineering internship with Celebal Technologies. The objective was to build a robust Medallion Architecture (Bronze-Silver-Gold) pipeline using PySpark, SparkSQL, and Databricks to process batch, incremental, and streaming retail data. 

## Architecture & Infrastructure
This pipeline leverages a **Unity Catalog Volume** (`/Volumes/workspace/default/retailstream_vol`) for all data ingestion, staging, and storage. Using a Volume rather than the default Databricks File System (DBFS) Workspace storage ensures enterprise-grade data governance, transactional safety for Delta tables, and secure checkpoint management for streaming tasks. 

### Pipeline Layers
*   **Bronze Layer:** Ingests raw data. Handles the initial batch load of January orders, incremental deduplicated loads of February orders, idempotent merges of late-arriving data, and continuous Auto Loader streaming of payment transactions.
*   **Silver Layer:** Cleans and enriches the data. Joins the Bronze order records with static dimension tables (Products, Customers, Stores), calculates core business metrics (revenue and margin), and drops unnecessary foreign keys. 
*   **Gold Layer:** Business-level analytics. Uses SparkSQL to aggregate data into final reporting tables, specifically a Monthly Sales Summary and a Payment Method Success Summary. 

---

## Technical Q&A

### (a) How did you handle deduplication in Task 2?
Deduplication during the incremental February load was handled using a `left_anti` join on the `order_id` column. I loaded the existing Bronze Delta table and performed an anti-join against the newly arriving February data. This ensured that only genuinely new orders were appended to the Bronze layer, filtering out any re-sent records before the write operation occurred. 

### (b) What happens if the Auto Loader checkpoint is deleted and the stream restarts?
The Auto Loader checkpoint directory stores the critical state of the stream, specifically tracking exactly which files in the landing zone have already been processed. If this checkpoint is deleted, the stream loses its historical state. Upon restarting, Auto Loader treats the landing zone as entirely new and will re-process every single CSV file currently in the folder from scratch, which would result in duplicated transaction records downstream. 

### (c) Why is MERGE preferred over overwrite for late arriving data?
The `MERGE` operation is preferred because it performs an idempotent upsert. If an `overwrite` operation were used for the late-arriving January data, it would completely wipe out the entire existing Bronze table and replace it with *only* those late records. By using `MERGE` with a `whenNotMatchedInsertAll()` condition, the pipeline safely inserts only the new, missing records while leaving the existing, correctly processed historical data intact and preventing duplicates if the job runs multiple times.

---

## Technologies & Frameworks Used
*   **Apache Spark (PySpark):** Core distributed data processing engine used for batch and incremental transformations.
*   **SparkSQL:** Utilized for Gold-layer aggregations and business logic.
*   **Delta Lake:** Provided ACID transactions, scalable metadata handling, and unified streaming/batch data processing for the Bronze, Silver, and Gold tables.
*   **Databricks Auto Loader (`cloudFiles`):** Enabled efficient, stateful streaming ingestion of raw transaction files from cloud storage.
*   **Unity Catalog:** Managed secure, governed access to the data volume (`retailstream_vol`) overriding legacy DBFS architectures.

---

## Repository Structure
```text
├── README.md                      # Project documentation and architectural decisions
├── RetailStream_Pipeline.ipynb    # Main Databricks pipeline notebook
└── data/                          # Sample dataset schemas (loaded via Unity Catalog Volume)
```