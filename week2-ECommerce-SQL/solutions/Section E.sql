/*
    Section E
*/


-- Q24. Classify products into price tiers using CASE.
SELECT
    product_name,
    unit_price,
    CASE
        WHEN unit_price < 1000 THEN 'Budget'
        WHEN unit_price BETWEEN 1000 AND 3000 THEN 'Mid-Range'
        WHEN unit_price > 3000 THEN 'Premium'
    END AS price_tier
FROM products;


-- Q25. Count how many orders are 'Delivered' vs 'Not Delivered'.
SELECT
    SUM(CASE WHEN status = 'Delivered' THEN 1 ELSE 0 END) AS Delivered,
    SUM(CASE WHEN status <> 'Delivered' THEN 1 ELSE 0 END) AS Not_Delivered
FROM orders;


-- Q26. Explain ACID properties.
-- A - Atomicity: A transaction is completed entirely or not at all.
-- C - Consistency: Ensures the database remains in a valid state before and after a transaction.
-- I - Isolation: Multiple transactions execute independently without affecting each other.
-- D - Durability: Once a transaction is committed, the changes are permanently saved.
/*
    Example:
    When a customer places an online order, the order is created,
    payment is processed, and the product stock is updated.
    If any of these steps fail, the entire transaction is rolled back.
    If all steps succeed, the order details, payment, and stock updates
    are permanently stored in the database.
*/


-- Q27. Write a SQL transaction.
START TRANSACTION;

-- Insert a new order
INSERT INTO orders
(order_id, customer_id, order_date, status, total_amount)
VALUES
(1011, 102, CURRENT_DATE, 'Pending', 1598.00);

-- Insert two order items
INSERT INTO order_items
(item_id, order_id, product_id, quantity, unit_price, discount_pct)
VALUES
(5016, 1011, 206, 1, 1299.00, 0),
(5017, 1011, 208, 1, 299.00, 0);

-- Update stock quantity
UPDATE products
SET stock_qty = stock_qty - 1
WHERE product_id = 206;

UPDATE products
SET stock_qty = stock_qty - 1
WHERE product_id = 208;

COMMIT;