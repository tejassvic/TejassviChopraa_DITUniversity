-- intermediate_queries.sql
-- Q4: Customers who placed orders but never had any item delivered
-- Q5: Products ordered but having more returns than purchases
-- Q6: Return rate per category

-- Q4: Customers who placed orders but never had any item delivered
SELECT
    o.customer_id,
    c.customer_name,
    COUNT(DISTINCT o.order_id) AS total_orders
FROM orders o
LEFT JOIN customers c ON o.customer_id = c.customer_id
WHERE o.customer_id != 'UNKNOWN'
GROUP BY o.customer_id, c.customer_name
HAVING SUM(CASE WHEN o.status = 'DELIVERED' THEN 1 ELSE 0 END) = 0
ORDER BY total_orders DESC;

-- Q5: Products ordered but having more returns than purchases
SELECT
    p.product_id,
    p.product_name,
    SUM(CASE WHEN oi.quantity > 0 THEN oi.quantity ELSE 0 END) AS total_purchased,
    ABS(SUM(CASE WHEN oi.quantity < 0 THEN oi.quantity ELSE 0 END)) AS total_returned,
    SUM(oi.quantity) AS net_quantity
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_id, p.product_name
HAVING ABS(SUM(CASE WHEN oi.quantity < 0 THEN oi.quantity ELSE 0 END))
       > SUM(CASE WHEN oi.quantity > 0 THEN oi.quantity ELSE 0 END)
ORDER BY total_returned DESC;

-- Q6: Return rate per category (returned_items / total_items)
SELECT
    p.category,
    SUM(CASE WHEN oi.quantity < 0 THEN ABS(oi.quantity) ELSE 0 END) AS returned_items,
    SUM(ABS(oi.quantity))                                           AS total_items,
    ROUND(
        COALESCE(
            SUM(CASE WHEN oi.quantity < 0 THEN ABS(oi.quantity) ELSE 0 END) * 1.0
            / NULLIF(SUM(ABS(oi.quantity)), 0),
            0
        ),
        4
    ) AS return_rate
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY return_rate DESC;