/* 
	SQL for database and table creation (same as given in file)
*/


-- Drop existing database (Removing copy)
DROP DATABASE IF EXISTS ecommerce_sales;

-- Create Database: ecommerce_sales
CREATE DATABASE ecommerce_sales;

-- Use Database
USE ecommerce_sales;

-- Table: customers
CREATE TABLE customers (
    customer_id INT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    city VARCHAR(50) NOT NULL,
    state VARCHAR(50) NOT NULL,
    join_date DATE NOT NULL,
    is_premium BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_customers_city
ON customers(city);

CREATE INDEX idx_customers_state
ON customers(state);

-- Table: products
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    brand VARCHAR(50) NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price > 0),
    stock_qty INT NOT NULL DEFAULT 0 CHECK (stock_qty >= 0)
);

CREATE INDEX idx_products_category
ON products(category);

-- Table: orders
CREATE TABLE orders (
    order_id INT PRIMARY KEY,
    customer_id INT NOT NULL,
    order_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Pending',
    total_amount DECIMAL(12,2) NOT NULL CHECK (total_amount >= 0),

    CONSTRAINT chk_orders_status
    CHECK (status IN ('Pending','Shipped','Delivered','Cancelled')),

    CONSTRAINT fk_orders_customer
    FOREIGN KEY (customer_id)
    REFERENCES customers(customer_id)
);

CREATE INDEX idx_orders_date
ON orders(order_date);

CREATE INDEX idx_orders_status
ON orders(status);

-- Table: order_items
CREATE TABLE order_items (
    item_id INT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NOT NULL,
    quantity INT NOT NULL CHECK (quantity > 0),
    unit_price DECIMAL(10,2) NOT NULL CHECK (unit_price > 0),
    discount_pct DECIMAL(5,2) DEFAULT 0
        CHECK (discount_pct BETWEEN 0 AND 100),

    CONSTRAINT fk_orderitems_order
    FOREIGN KEY (order_id)
    REFERENCES orders(order_id),

    CONSTRAINT fk_orderitems_product
    FOREIGN KEY (product_id)
    REFERENCES products(product_id)
);

-- Verify Tables
SHOW TABLES;

DESCRIBE customers;
DESCRIBE products;
DESCRIBE orders;
DESCRIBE order_items;