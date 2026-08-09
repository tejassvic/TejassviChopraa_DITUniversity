-- ============================================================================
-- basic_queries.sql
--
-- Basic analytical queries for the E-Commerce Order Analytics System.
--
-- These queries demonstrate fundamental SQL skills:
--     * JOINs across three tables,
--     * aggregation with GROUP BY,
--     * ordering / limiting results,
--     * string formatting of dates.
--
-- Revenue is always calculated with the same formula:
--
--     quantity * unit_price * (1 - discount_percent / 100.0)
--
-- Negative quantity rows (returns) naturally reduce revenue, which is the
-- desired behaviour for a real order analytics system.
-- ============================================================================

-- ----------------------------------------------------------------------------
-- QUERY 1 : Total revenue per category
-- ----------------------------------------------------------------------------
SELECT
    p.category,
    ROUND(
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)),
        2
    ) AS total_revenue
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.category
ORDER BY total_revenue DESC;

-- ----------------------------------------------------------------------------
-- QUERY 2 : Top 10 customers by total order value
-- ----------------------------------------------------------------------------
SELECT
    c.customer_id,
    c.customer_name,
    ROUND(
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)),
        2
    ) AS total_order_value
FROM order_items oi
JOIN orders o   ON oi.order_id = o.order_id
JOIN customers c ON o.customer_id = c.customer_id
GROUP BY c.customer_id, c.customer_name
ORDER BY total_order_value DESC
LIMIT 10;

-- ----------------------------------------------------------------------------
-- QUERY 3 : Month-wise order count for the last 12 months
-- ----------------------------------------------------------------------------
SELECT
    strftime('%Y-%m', order_date)                AS order_month,
    COUNT(*)                                     AS order_count
FROM orders
WHERE order_date >= datetime(
        (SELECT MAX(order_date) FROM orders),
        '-11 months',
        'start of month'
      )
GROUP BY order_month
ORDER BY order_month ASC;