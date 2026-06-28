# E-Commerce Sales Database

## Overview

This project is my Week 2 SQL assignment for the **Celebal Summer Internship 2026**.

The objective of this assignment is to design a relational database for a fictional e-commerce company called **ShopEase** and write SQL queries to answer different business-related questions. The database contains information about customers, products, orders, and order items.

The assignment covers SQL fundamentals as well as more advanced concepts such as filtering, aggregation, joins, constraints, CASE statements, and transactions.

---

## Database Schema

```
customers ──(1:N)──▶ orders ──(1:N)──▶ order_items ◀──(1:N)── products
```

### Tables Used

| Table       | Primary Key |
| ----------- | ----------- |
| customers   | customer_id |
| products    | product_id  |
| orders      | order_id    |
| order_items | item_id     |

---

## Project Structure

```
Week2_ECommerce_SQL/
│
├── README.md
│
├── schema/
│   └── create_database.sql
│
├── data/
│   └── insert_data.sql
│
└── solutions/
    ├── section_A.sql
    ├── section_B.sql
    ├── section_C.sql
    ├── section_D.sql
    └── section_E.sql
```

---

## How to Run

1. Open **MySQL Workbench** (or any SQL-compatible database).
2. Run `schema/create_database.sql` to create the database and tables.
3. Run `data/insert_data.sql` to insert the sample data.
4. Execute the SQL files inside the `solutions` folder in the following order:

   * Section A
   * Section B
   * Section C
   * Section D
   * Section E

> **Note:** Some questions intentionally generate errors (such as UNIQUE, CHECK, and FOREIGN KEY constraint violations) to demonstrate how database constraints work. Execute those queries individually if you want to observe the expected errors.

---

## Topics Covered

### Section A – SQL Basics

* SELECT statements
* DISTINCT
* Primary Keys
* UNIQUE constraint
* CHECK constraint

### Section B – Filtering & Optimization

* WHERE clause
* AND
* BETWEEN
* Indexes
* SARGable queries

### Section C – Aggregation

* COUNT()
* SUM()
* AVG()
* MIN()
* MAX()
* GROUP BY
* HAVING

### Section D – Joins & Relationships

* INNER JOIN
* LEFT JOIN
* RIGHT JOIN
* Three-table JOIN
* Foreign Keys

### Section E – Advanced SQL

* CASE statements
* Conditional aggregation
* ACID properties
* Transactions
* COMMIT
* ROLLBACK

---

## Tools Used

* MySQL Workbench
* SQL (MySQL compatible)
* Standard SQL syntax

---

## Learning Outcomes

Through this assignment, I learned how to:

* Design and create relational database tables.
* Apply primary keys, foreign keys, and constraints.
* Write queries to filter and retrieve data.
* Perform data aggregation using SQL functions.
* Work with different types of joins.
* Use CASE statements for conditional logic.
* Understand ACID properties and SQL transactions.