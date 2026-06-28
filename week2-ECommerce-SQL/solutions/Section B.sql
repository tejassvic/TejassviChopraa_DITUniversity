/*
    Section B
*/


-- Q7. Retrieve all orders with status = 'Delivered'.
SELECT *
FROM orders
WHERE status = 'Delivered';


-- Q8. Find all products in the 'Electronics' category with a unit_price greater than ₹2000.
SELECT *
FROM products
WHERE category = 'Electronics'
  AND unit_price > 2000;


-- Q9. List all customers who joined in the year 2024 and belong to the state 'Maharashtra'.
SELECT *
FROM customers
WHERE state = 'Maharashtra'
  AND join_date BETWEEN '2024-01-01' AND '2024-12-31';


-- Q10. Find all orders placed between '2024-08-10' and '2024-08-25' (inclusive) that are NOT cancelled.
SELECT *
FROM orders
WHERE order_date BETWEEN '2024-08-10' AND '2024-08-25'
  AND status <> 'Cancelled';


-- Q11. Explain what the index idx_orders_date does.
-- The idx_orders_date index speeds up queries that filter or sort records using the order_date column.
-- It reduces the need for a full table scan, improving query performance.

-- Sample query that benefits from this index:
SELECT *
FROM orders
WHERE order_date BETWEEN '2024-08-01' AND '2024-08-31';


-- Q12. Would the index be used with YEAR(join_date)?
SELECT *
FROM customers
WHERE YEAR(join_date) = 2024;

-- Result:
-- No. Applying the YEAR() function to join_date prevents the database from using the index efficiently.

-- Index-friendly (SARGable) query:
SELECT *
FROM customers
WHERE join_date >= '2024-01-01'
  AND join_date < '2025-01-01';