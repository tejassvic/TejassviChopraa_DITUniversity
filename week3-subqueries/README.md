# Superstore Sales Analysis

## Overview

This project is my Week 3 SQL assignment for the Celebal Summer Internship 2026. 
The objective of this assignment is to design a normalized relational database from the flat Superstore dataset and write advanced SQL queries to answer business-related questions. The database contains information about customers, products, and individual orders.

This assignment focuses heavily on moving beyond basic SQL by applying **Subqueries**, **Common Table Expressions (CTEs)**, and **Window Functions** to perform complex data rankings and aggregations.

## Database Schema

The raw dataset was normalized into three distinct tables:
`customers` ──(1:N)──▶ `orders` ◀──(N:1)── `products`

*Note on design:* Location data (City, State, Region, Postal Code) was kept in the `orders` table rather than `customers`, because the same customer can ship orders to different locations. This prevents primary key violations.

## Tables Used

| Table | Primary Key | Description |
| :--- | :--- | :--- |
| `customers` | `customer_id` | Unique customer details (Name, Segment) |
| `products` | `product_id` | Unique product details (Name, Category, Sub-Category) |
| `orders` | `row_id` | Order transactions, shipping info, and financials |

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