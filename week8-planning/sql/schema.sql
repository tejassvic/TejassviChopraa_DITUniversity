-- ============================================================================
-- schema.sql
--
-- SQLite schema for the E-Commerce Order Analytics System.
--
-- The schema mirrors the cleaned CSV structure and adds useful constraints:
--     * PRIMARY KEY on every natural/surrogate key,
--     * FOREIGN KEY relationships (enforced when PRAGMA foreign_keys = ON),
--     * NOT NULL on all required analytical columns.
--
-- The database file itself (ecommerce.db) is created by load_database.py,
-- which executes this script.
-- ============================================================================

PRAGMA foreign_keys = ON;

-- ----------------------------------------------------------------------------
-- customers
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS customers (
    customer_id       TEXT PRIMARY KEY,              -- e.g. CUST-0001
    customer_name     TEXT NOT NULL,
    email             TEXT NOT NULL,
    registration_date TEXT NOT NULL,                 -- YYYY-MM-DD HH:MM:SS
    customer_type     TEXT NOT NULL CHECK (
                          customer_type IN ('REGULAR', 'PREMIUM', 'VIP')
                      )
);

-- ----------------------------------------------------------------------------
-- products
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS products (
    product_id   TEXT PRIMARY KEY,                   -- e.g. PRD-0001
    product_name TEXT NOT NULL,
    category     TEXT NOT NULL,
    subcategory  TEXT NOT NULL,
    cost_price   REAL NOT NULL CHECK (cost_price >= 0)
);

-- ----------------------------------------------------------------------------
-- orders
--
-- customer_id may be 'UNKNOWN' for orders where the original source data was
-- missing a customer reference.  We therefore do not enforce a hard FK from
-- orders -> customers, because 'UNKNOWN' is not a real customer row.
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS orders (
    order_id    TEXT PRIMARY KEY,                    -- e.g. ORD-00001
    customer_id TEXT DEFAULT 'UNKNOWN',
    order_date  TEXT NOT NULL,                       -- YYYY-MM-DD HH:MM:SS
    status      TEXT NOT NULL CHECK (
                    status IN ('PLACED', 'SHIPPED', 'DELIVERED', 'CANCELLED', 'RETURNED')
                ),
    region_code TEXT NOT NULL
);

-- ----------------------------------------------------------------------------
-- order_items
-- ----------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS order_items (
    item_id          TEXT PRIMARY KEY,               -- e.g. ITM-000001
    order_id         TEXT NOT NULL,
    product_id       TEXT NOT NULL,
    quantity         INTEGER NOT NULL,               -- negative = return
    unit_price       REAL NOT NULL CHECK (unit_price >= 0),
    discount_percent REAL NOT NULL CHECK (
                         discount_percent BETWEEN 0 AND 100
                     ),
    FOREIGN KEY (order_id)   REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
);

-- ============================================================================
-- Indexes
--
-- Indexes are created on the foreign-key columns and on the columns that are
-- frequently used in WHERE / GROUP BY / ORDER BY clauses by the analytics
-- queries in basic_queries.sql, intermediate_queries.sql and
-- advanced_queries.sql.
-- ============================================================================

CREATE INDEX IF NOT EXISTS idx_orders_customer_id   ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_order_date    ON orders(order_date);
CREATE INDEX IF NOT EXISTS idx_orders_status        ON orders(status);
CREATE INDEX IF NOT EXISTS idx_orders_region_code   ON orders(region_code);

CREATE INDEX IF NOT EXISTS idx_order_items_order_id    ON order_items(order_id);
CREATE INDEX IF NOT EXISTS idx_order_items_product_id  ON order_items(product_id);

CREATE INDEX IF NOT EXISTS idx_products_category    ON products(category);

CREATE INDEX IF NOT EXISTS idx_customers_type       ON customers(customer_type);