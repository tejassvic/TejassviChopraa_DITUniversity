-- advanced_queries.sql
-- Q7-Q16: Advanced window function / CTE queries
-- QB: Market basket analysis

-- Q7: Running totals per region ordered by date
SELECT
    o.region_code,
    o.order_date,
    ROUND(
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0))
            OVER (PARTITION BY o.region_code ORDER BY o.order_date, o.order_id),
        2
    ) AS daily_revenue,
    ROUND(
        SUM(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)))
            OVER (PARTITION BY o.region_code ORDER BY o.order_date, o.order_id
                  ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW),
        2
    ) AS running_total
FROM orders o
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.region_code, o.order_date, o.order_id
ORDER BY o.region_code, o.order_date, o.order_id;

-- Q8: DENSE_RANK revenue ranking within category
WITH product_revenue AS (
    SELECT
        p.category,
        p.product_name,
        ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)), 2)
            AS total_revenue
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY p.category, p.product_name
)
SELECT
    category,
    product_name,
    total_revenue,
    DENSE_RANK() OVER (PARTITION BY category ORDER BY total_revenue DESC) AS rank_in_category
FROM product_revenue
ORDER BY category, rank_in_category;

-- Q9: LAG/LEAD days between consecutive orders + At Risk flag
WITH order_gaps AS (
    SELECT
        customer_id,
        order_date,
        LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date)
            AS previous_order_date,
        ROUND(
            julianday(order_date)
            - julianday(LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date)),
            2
        ) AS days_gap
    FROM orders
    WHERE customer_id != 'UNKNOWN'
),
customer_average AS (
    SELECT
        customer_id,
        AVG(days_gap) AS avg_gap_days
    FROM order_gaps
    WHERE days_gap IS NOT NULL
    GROUP BY customer_id
)
SELECT
    og.customer_id,
    og.order_date,
    og.previous_order_date,
    og.days_gap,
    CASE WHEN ca.avg_gap_days > 30 THEN 'At Risk' ELSE 'Healthy' END AS customer_status
FROM order_gaps og
JOIN customer_average ca USING (customer_id)
ORDER BY og.customer_id, og.order_date;

-- Q10: Multi-level CTE monthly customer segmentation
WITH monthly_customer_revenue AS (
    SELECT
        o.customer_id,
        strftime('%Y-%m', o.order_date) AS month,
        ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)), 2)
            AS monthly_revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.customer_id != 'UNKNOWN'
    GROUP BY o.customer_id, strftime('%Y-%m', o.order_date)
),
customer_segments AS (
    SELECT
        customer_id,
        month,
        monthly_revenue,
        CASE
            WHEN monthly_revenue > 10000 THEN 'High'
            WHEN monthly_revenue BETWEEN 5000 AND 10000 THEN 'Medium'
            ELSE 'Low'
        END AS revenue_segment
    FROM monthly_customer_revenue
)
SELECT
    month,
    revenue_segment,
    COUNT(DISTINCT customer_id) AS customer_count
FROM customer_segments
GROUP BY month, revenue_segment
ORDER BY month, revenue_segment;

-- Q11: NTILE quartile customer segmentation
WITH customer_lifetime_value AS (
    SELECT
        o.customer_id,
        ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)), 2)
            AS total_value
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.customer_id != 'UNKNOWN'
    GROUP BY o.customer_id
)
SELECT
    customer_id,
    total_value,
    NTILE(4) OVER (ORDER BY total_value DESC) AS quartile,
    CASE NTILE(4) OVER (ORDER BY total_value DESC)
        WHEN 1 THEN 'Platinum'
        WHEN 2 THEN 'Gold'
        WHEN 3 THEN 'Silver'
        WHEN 4 THEN 'Bronze'
    END AS quartile_label
FROM customer_lifetime_value
ORDER BY total_value DESC;

-- Q12: Year-over-Year revenue comparison
WITH monthly_revenue AS (
    SELECT
        CAST(strftime('%Y', order_date) AS INTEGER) AS year,
        CAST(strftime('%m', order_date) AS INTEGER) AS month,
        ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)), 2)
            AS revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY year, month
)
SELECT
    cur.year,
    cur.month,
    cur.revenue,
    prev.revenue AS prev_year_revenue,
    CASE
        WHEN prev.revenue IS NULL THEN NULL
        ELSE ROUND(
            (cur.revenue - prev.revenue) * 100.0 / NULLIF(prev.revenue, 0),
            2
        )
    END AS yoy_growth_percent
FROM monthly_revenue cur
LEFT JOIN monthly_revenue prev
       ON cur.month = prev.month
      AND prev.year = cur.year - 1
ORDER BY cur.year, cur.month;

-- Q13: First/Last Value category shift per customer
WITH customer_category_orders AS (
    SELECT o.customer_id, p.category, o.order_date
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p    ON oi.product_id = p.product_id
    WHERE o.customer_id != 'UNKNOWN'
),
first_last AS (
    SELECT
        customer_id,
        FIRST_VALUE(category) OVER (
            PARTITION BY customer_id ORDER BY order_date, category
        ) AS first_category,
        LAST_VALUE(category) OVER (
            PARTITION BY customer_id
            ORDER BY order_date, category
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS last_category
    FROM customer_category_orders
)
SELECT DISTINCT
    customer_id,
    first_category,
    last_category,
    CASE WHEN first_category != last_category THEN 'Yes' ELSE 'No' END AS category_shift
FROM first_last
ORDER BY customer_id;

-- Q14: Cumulative distribution of customer revenue
WITH customer_revenue AS (
    SELECT
        o.customer_id,
        ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)), 2)
            AS revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.customer_id != 'UNKNOWN'
    GROUP BY o.customer_id
),
total AS (
    SELECT SUM(revenue) AS grand_total FROM customer_revenue
)
SELECT
    cr.customer_id,
    cr.revenue,
    ROUND(
        SUM(cr.revenue) OVER (
            ORDER BY cr.revenue DESC
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ),
        2
    ) AS cumulative_revenue,
    ROUND(
        100.0 * SUM(cr.revenue) OVER (
            ORDER BY cr.revenue DESC
            ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
        ) / t.grand_total,
        2
    ) AS cumulative_percent
FROM customer_revenue cr
CROSS JOIN total t
ORDER BY cr.revenue DESC;

-- Q15: Complex CTE - cohort retention analysis
WITH customer_cohorts AS (
    SELECT
        customer_id,
        strftime('%Y-%m', registration_date) AS cohort_month
    FROM customers
    WHERE customer_id != 'UNKNOWN'
),
activity AS (
    SELECT DISTINCT
        oc.customer_id,
        oc.cohort_month,
        CAST(
            (CAST(strftime('%Y', o.order_date) AS INTEGER) * 12
             + CAST(strftime('%m', o.order_date) AS INTEGER))
            - (CAST(strftime('%Y', oc.cohort_month || '-01') AS INTEGER) * 12
               + CAST(strftime('%m', oc.cohort_month || '-01') AS INTEGER))
            AS INTEGER
        ) AS month_offset
    FROM customer_cohorts oc
    JOIN orders o ON o.customer_id = oc.customer_id
),
cohort_sizes AS (
    SELECT
        cohort_month,
        COUNT(DISTINCT customer_id) AS cohort_size
    FROM customer_cohorts
    GROUP BY cohort_month
)
SELECT
    a.cohort_month,
    cs.cohort_size,
    COALESCE(SUM(CASE WHEN a.month_offset = 0 THEN 1 ELSE 0 END), 0) AS month0,
    COALESCE(SUM(CASE WHEN a.month_offset = 1 THEN 1 ELSE 0 END), 0) AS month1,
    COALESCE(SUM(CASE WHEN a.month_offset = 2 THEN 1 ELSE 0 END), 0) AS month2,
    COALESCE(SUM(CASE WHEN a.month_offset = 3 THEN 1 ELSE 0 END), 0) AS month3,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN a.month_offset = 1 THEN a.customer_id END)
          / NULLIF(cs.cohort_size, 0), 2) AS retention_month1,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN a.month_offset = 2 THEN a.customer_id END)
          / NULLIF(cs.cohort_size, 0), 2) AS retention_month2,
    ROUND(100.0 * COUNT(DISTINCT CASE WHEN a.month_offset = 3 THEN a.customer_id END)
          / NULLIF(cs.cohort_size, 0), 2) AS retention_month3
FROM activity a
JOIN cohort_sizes cs USING (cohort_month)
GROUP BY a.cohort_month, cs.cohort_size
ORDER BY a.cohort_month;

-- Q16: Self-join with window function - product lift analysis
WITH product_monthly AS (
    SELECT
        p.product_id,
        p.product_name,
        p.category,
        strftime('%Y-%m', o.order_date) AS month,
        ROUND(SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)), 2)
            AS monthly_revenue
    FROM order_items oi
    JOIN orders o    ON oi.order_id = o.order_id
    JOIN products p  ON oi.product_id = p.product_id
    GROUP BY p.product_id, p.product_name, p.category, strftime('%Y-%m', o.order_date)
)
SELECT
    pm.product_name,
    pm.category,
    pm.month,
    pm.monthly_revenue,
    ROUND(AVG(pm.monthly_revenue) OVER (PARTITION BY pm.category, pm.month), 2)
        AS category_monthly_avg,
    ROUND(
        100.0 * (pm.monthly_revenue - AVG(pm.monthly_revenue) OVER (PARTITION BY pm.category, pm.month))
        / NULLIF(AVG(pm.monthly_revenue) OVER (PARTITION BY pm.category, pm.month), 0),
        2
    ) AS pct_above_category_avg,
    RANK() OVER (PARTITION BY pm.category, pm.month ORDER BY pm.monthly_revenue DESC)
        AS month_rank_in_category
FROM product_monthly pm
ORDER BY pm.category, pm.month, pm.monthly_revenue DESC;

-- QB: Market basket analysis - products frequently bought together
SELECT
    pa.product_name AS product_a,
    pb.product_name AS product_b,
    COUNT(*) AS times_bought_together
FROM order_items oia
JOIN order_items oib
       ON oia.order_id = oib.order_id
      AND oia.product_id < oib.product_id
JOIN products pa ON oia.product_id = pa.product_id
JOIN products pb ON oib.product_id = pb.product_id
GROUP BY pa.product_name, pb.product_name
ORDER BY times_bought_together DESC
LIMIT 20;