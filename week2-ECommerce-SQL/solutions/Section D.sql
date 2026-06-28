/*
    Section D
*/


-- Q19. Write an INNER JOIN query to display each order along with the customer's
-- first_name and last_name.
SELECT
    o.order_id,
    o.order_date,
    c.first_name,
    c.last_name,
    o.total_amount
FROM orders o
INNER JOIN customers c
ON o.customer_id = c.customer_id;


-- Q20. Using a LEFT JOIN, list ALL customers and their orders (if any).
-- Customers with no orders should still appear with NULL values.
SELECT
    c.customer_id,
    c.first_name,
    c.last_name,
    o.order_id,
    o.order_date,
    o.total_amount
FROM customers c
LEFT JOIN orders o
ON c.customer_id = o.customer_id;


-- Q21. Write a query using JOINs across three tables
-- (orders → order_items → products).
SELECT
    o.order_id,
    p.product_name,
    oi.quantity,
    oi.unit_price,
    oi.discount_pct
FROM orders o
JOIN order_items oi
ON o.order_id = oi.order_id
JOIN products p
ON oi.product_id = p.product_id;


-- Q22. Explain the difference between LEFT JOIN and RIGHT JOIN.
-- LEFT JOIN returns all records from the left table and matching records from the right table.
-- RIGHT JOIN returns all records from the right table and matching records from the left table.
-- FULL OUTER JOIN returns all records from both tables, whether they have matching values or not.

-- Example of LEFT JOIN:
SELECT
    c.customer_id,
    c.first_name,
    o.order_id
FROM customers c
LEFT JOIN orders o
ON c.customer_id = o.customer_id;

-- Example of RIGHT JOIN:
SELECT
    c.customer_id,
    c.first_name,
    o.order_id
FROM customers c
RIGHT JOIN orders o
ON c.customer_id = o.customer_id;


-- Q23. Identify all Foreign Key relationships in the schema.
-- orders.customer_id      -> customers.customer_id
-- order_items.order_id    -> orders.order_id
-- order_items.product_id  -> products.product_id
/*  
    If an order is inserted with customer_id = 999 (which does not exist),
    the database will throw a FOREIGN KEY constraint violation and the row
    will not be inserted.
*/

-- Example:
INSERT INTO orders
(order_id, customer_id, order_date, status, total_amount)
VALUES
(1011, 999, '2024-09-01', 'Pending', 1000.00);

-- Result:
-- ERROR: Cannot add or update a child row: a foreign key constraint fails.