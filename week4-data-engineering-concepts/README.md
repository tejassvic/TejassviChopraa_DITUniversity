# Azure Cloud Fundamentals & Data Pipeline using ADF

**Author:** Tejassvi Chopraa  
**Subscription:** Azure for Students (DIT University)  
**Dataset:** Superstore Dataset — Kaggle  

---

## Project Overview

This project is part of my Week 4 assignment, where I worked with Microsoft Azure and Azure Data Factory (ADF).

The main aim of this assignment was to understand the basic concepts of Azure cloud services and create a simple data pipeline using Azure Data Factory. I started by creating a resource group and storage account, uploaded the Superstore dataset to Blob Storage, connected it with ADF, and finally created a pipeline to check and copy the CSV file.

This assignment helped me understand Linked Services, Datasets, Get Metadata activity, Copy Data activity, pipelines, and IAM roles in Azure.

---

## Task 1 — Creating a Resource Group

For the first task, I created a Resource Group named:

`celebal_intern`

A Resource Group is used to keep related Azure resources together. It makes the resources easier to manage and organize.

All the Azure resources used in this assignment were created and managed under this setup.

---

## Task 2 — Setting up Azure Blob Storage

For this task, I created an Azure Storage Account named:

`cttejassvi`

Inside the storage account, I created a Blob container called:

`assignment-files`

I then uploaded the following dataset:

`Sample - Superstore.csv`

The Superstore dataset contains sales-related data such as orders, customers, products, categories, sales, quantity, discount, and profit.

The CSV file was uploaded successfully and was then used as the source file for the Azure Data Factory pipeline.

---

## Task 3 — Azure Data Factory Basics

In this task, I created an Azure Data Factory instance named:

`tejassviintern`

After creating the Data Factory, I opened ADF Studio and explored its main sections:

- **Author** — used to create pipelines and datasets.
- **Monitor** — used to check pipeline execution and status.
- **Manage** — used to configure Linked Services and other Data Factory settings.

### Creating the Linked Service

I created an Azure Blob Storage Linked Service named:

`LinkedService_BlobStorage`

The Linked Service was used to connect Azure Data Factory with my Azure Storage Account.

After configuring the connection, I tested it and the Linked Service was created successfully.

### Creating the Datasets

I created two DelimitedText datasets:

- `SourceDataset`
- `DestinationDataset`

The `SourceDataset` points to:

`assignment-files/Sample - Superstore.csv`

The `DestinationDataset` is used to store the copied CSV file.

Both datasets use `LinkedService_BlobStorage` to connect with Azure Blob Storage.

### Get Metadata Activity

I also added a Get Metadata activity named:

`CheckFileExists`

The activity uses `SourceDataset` and checks whether the source file exists before the copy operation starts.

I selected the `Exists` field in the Get Metadata activity.

This helped me understand how metadata activities can be used to validate a source file before performing another operation.

---

## Task 4 — Creating the Data Pipeline

For this task, I created a pipeline named:

`CopyCSV_Pipeline`

The pipeline contains two activities:

1. `CheckFileExists` — Get Metadata activity
2. `Copy data` — Copy Data activity

The `CheckFileExists` activity runs first and checks the source CSV file.

After the metadata activity succeeds, the `Copy data` activity starts.

The pipeline flow is:

```text
[Get Metadata: CheckFileExists] ----Success----> [Copy Data]
```

The Copy Data activity reads the Superstore CSV file from the source dataset and copies it to the destination dataset.

Since I was working with only one CSV file, I did not need to use a ForEach activity.

---

## Task 5 — Running the Pipeline

After completing the pipeline configuration, I ran the pipeline using the Debug option in Azure Data Factory.

The pipeline executed successfully.

Both activities showed the status:

`Succeeded`

The execution order was:

```text
CheckFileExists
       |
       v
   Copy data
```

The Get Metadata activity first checked whether the file existed. After it succeeded, the Copy Data activity copied the CSV file.

The pipeline completed successfully and the output showed that both activities were executed without errors.

---

## Task 6 — IAM Roles

In this task, I explored Access Control (IAM) for the Azure Storage Account.

The following roles were visible in the IAM role assignments:

| Role | Assigned To | Purpose |
| --- | --- | --- |
| Owner | My Azure user account | Full access to manage Azure resources |
| Contributor | `tejassviintern` Managed Identity | Allows the Data Factory identity to manage the resource |
| Reader | `tejassviintern` Managed Identity | Provides read access to the resource |
| Storage Blob Data Contributor | `tejassviintern` Managed Identity | Allows reading and writing Blob Storage data |

The `Storage Blob Data Contributor` role is especially useful because it allows Azure Data Factory to access Blob Storage using its Managed Identity.

This is more secure than directly sharing storage credentials in a real project.

---

## Mini Project — End-to-End CSV Copy Pipeline

For the mini project, I combined the Get Metadata and Copy Data activities into a single pipeline.

The final pipeline was:

```text
[CheckFileExists] ----Success----> [Copy data]
```

First, the `CheckFileExists` activity checks whether the Superstore CSV file exists in the Blob container.

If the activity succeeds, the `Copy data` activity copies the file.

The copied file was created as:

`copied.csv`

The final Blob Storage container contained both:

```text
Sample - Superstore.csv
copied.csv
```

This confirmed that the pipeline successfully copied the source CSV file.

---

## What I Learned

While completing this assignment, I learned how to:

- Create and manage Azure Resource Groups.
- Create an Azure Storage Account and Blob container.
- Upload CSV files to Azure Blob Storage.
- Create an Azure Data Factory instance.
- Connect ADF with Blob Storage using a Linked Service.
- Create source and destination datasets.
- Use the Get Metadata activity to check if a file exists.
- Use the Copy Data activity to copy CSV files.
- Connect multiple pipeline activities using the Success condition.
- Run and debug Azure Data Factory pipelines.
- Understand basic IAM roles and Managed Identity access.

---

## Conclusion

This assignment gave me practical experience with Microsoft Azure and Azure Data Factory.

I created an Azure Blob Storage setup, connected it with Azure Data Factory, and built a simple pipeline that first checks whether a CSV file exists and then copies it.

The pipeline executed successfully, and the copied file `copied.csv` was available in the Blob Storage container.

Overall, this assignment helped me understand the basic workflow of a cloud-based data pipeline and how different Azure services can work together.
