# Superstore Sales Analysis

## Overview

This project is my Week 3 SQL assignment for the Celebal Summer Internship 2026.

The objective of this assignment is to design a normalized relational database from the flat Superstore dataset and write advanced SQL queries to answer business-related questions. The database contains information about customers, products, and individual orders.

This assignment focuses heavily on moving beyond basic SQL by applying **Subqueries**, **Common Table Expressions (CTEs)**, and **Window Functions** to perform complex data rankings and aggregations.

---

## Database Schema

The raw dataset was normalized into three distinct tables:

```text
customers (1:N) ─────► orders ◄───── (N:1) products
```

**Note on design:**  
Location data (City, State, Region, Postal Code) was kept in the `orders` table rather than `customers`, because the same customer can ship orders to different locations. This prevents primary key violations.

---

## Tables Used

| Table | Primary Key | Description |
|--------|-------------|-------------|
| `customers` | `customer_id` | Unique customer details (Name, Segment) |
| `products` | `product_id` | Unique product details (Name, Category, Sub-Category) |
| `orders` | `row_id` | Order transactions, shipping information, and financial data |

---

## Project Structure

```text
week3-subqueries/
│
├── dataset/
│   └── superstore.csv
│
└── notebook and sql/
    ├── customer_sales_insights.sql
    └── superstore_analysis.ipynb
```

---

## Topics Covered

### Step 1 – Database Normalization & Cleaning

- Migrating a flat CSV into a relational database using **pandas** and **SQLAlchemy**
- Handling duplicate records using `GROUP BY` and `MAX()` to satisfy `PRIMARY KEY` constraints
- Using `SELECT DISTINCT` while inserting data

### Step 2 – Advanced SQL Querying

#### Subqueries

- Filtering records based on aggregate values
- Example: Finding orders with sales above the overall average

#### Common Table Expressions (CTEs)

- Using the `WITH` clause to create readable temporary result sets
- Calculating total customer sales before applying filters

#### Window Functions

- `RANK() OVER (ORDER BY ...)` to rank customers based on lifetime sales
- `ROW_NUMBER() OVER (PARTITION BY ...)` to assign sequence numbers to each customer's orders

### Step 3 – Business Insights

- Combining `JOIN`, `CTE`, and Window Functions within a single query
- Identifying retention-risk customers using `HAVING COUNT() = 1`

---

## Key Business Insights

Executing the final queries produced the following results:

- **Dataset Scale:** 793 unique customers and 5,009 distinct orders
- **Average Line-Item Sale:** **$229.86**
- **Retention Risk:** 12 customers (~1.5%) placed only one order
- **Top Customer:** Sean Miller with **$25,043.07** total sales
- **Highest Single Order:** **$22,638.48**
- **Lowest Customers:**
  - Thais Sissman — **$4.84**
  - Lela Donovan — **$5.30**

---

## Tools Used

- MySQL Community Server 8.0+
- MySQL Workbench
- Jupyter Notebook
- Python
  - pandas
  - SQLAlchemy
  - PyMySQL

---

## Learning Outcomes

Through this assignment, I learned how to:

- Normalize flat datasets into relational database tables
- Handle duplicate records while maintaining strict primary key constraints
- Optimize SQL queries to avoid inefficient correlated subqueries
- Write cleaner SQL using Common Table Expressions (CTEs)
- Apply Window Functions (`RANK()` and `ROW_NUMBER()`) for advanced analytics
- Extract meaningful business insights from transactional datasets