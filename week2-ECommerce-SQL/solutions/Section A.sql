/*
    Section A
*/


-- Q1. Display all columns and rows from the customers table.
SELECT *
FROM customers;


-- Q2. Retrieve only the first_name, last_name, and city of all customers.
SELECT first_name, last_name, city
FROM customers;


-- Q3. List all unique categories available in the products table.
SELECT DISTINCT category
FROM products;


-- Q4. Identify the Primary Key of each table.
-- customers    -> customer_id
-- products     -> product_id
-- orders       -> order_id
-- order_items  -> item_id
-- A PRIMARY KEY uniquely identifies each record in a table. It cannot contain NULL values and duplicate values are not allowed.


-- Q5. Constraints on the email column.
-- The email column has: 1. NOT NULL 2. UNIQUE
INSERT INTO customers (customer_id, first_name, last_name, email, city, state, join_date, is_premium)
VALUES (109, 'Rahul', 'Sharma', 'aarav.s@email.com', 'Delhi', 'Delhi', '2024-09-01', FALSE);
-- Result: ERROR 1062 (23000): Duplicate entry 'aarav.s@email.com' for key 'customers.email'


-- Q6. Insert a product with unit_price = -50.
INSERT INTO products (product_id, product_name, category, brand, unit_price, stock_qty)
VALUES (209, 'Test Product', 'Electronics', 'TestBrand', -50, 100);
-- Result: ERROR CHECK constraint 'unit_price > 0' failed.
-- The CHECK constraint CHECK (unit_price > 0) prevents negative prices.