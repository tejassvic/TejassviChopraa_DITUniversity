# E-Commerce Order Analytics System

This project is an **end-to-end data engineering and analytics project** created using **Python and SQLite**. The aim of the project is to generate sample e-commerce order data, clean the data, store it in a database, run SQL analysis, and generate business reports.

---

## Project Objectives

The main goals of this project are:

* Generate realistic e-commerce data such as customers, products, orders, and order items.
* Add some intentional data errors to simulate real-world dirty data.
* Clean and validate the data using Python.
* Store the cleaned data in a SQLite database.
* Perform basic and advanced SQL analysis.
* Create a command-line report generator.
* Test important edge cases and verify the output.

---

## Technologies Used

| Technology   | Purpose                                   |
| ------------ | ----------------------------------------- |
| Python 3.10+ | Main programming language                 |
| pandas       | Data cleaning and CSV handling            |
| Faker        | Generating fake customer and product data |
| SQLite       | Database storage and SQL analysis         |
| sqlite3      | Connecting Python with SQLite             |
| pathlib      | File and folder handling                  |

**Note:** `sqlite3` comes with Python, so it does not need to be installed separately.

---

## Project Folder Structure

```text
week8-planning/

├── data/
│   ├── raw/
│   └── cleaned/
├── sql/
├── reports/
├── src/
├── tests/
├── ecommerce.db
├── requirements.txt
└── README.md
```

* `data/raw/` contains the generated raw CSV files.
* `data/cleaned/` contains cleaned CSV files.
* `sql/` contains schema and analytics queries.
* `reports/` stores generated reports.
* `src/` contains all Python scripts.
* `tests/` contains edge-case tests.

---

## Example Output

The project generates summaries such as:

* total orders,
* total revenue,
* unique customers,
* top-selling products,
* comparison with the previous period.

Since the data is randomly generated, the exact numbers may change, although a fixed random seed is used for reproducibility.

---

## Assumptions

* All dates are stored in `YYYY-MM-DD HH:MM:SS` format.
* Missing customer IDs are replaced with `UNKNOWN`.
* Negative quantities are treated as product returns.
* Revenue is calculated after applying discounts.
* Discount values must remain between 0 and 100.

---

## Conclusion

This project helped me understand the complete workflow of a small data engineering project, including **data generation, data cleaning, database loading, SQL analytics, report generation, and testing**.
