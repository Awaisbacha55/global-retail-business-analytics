-- ====================================================================
-- Global Retail Business Analytics & Decision Intelligence
-- PostgreSQL Database Schema Definition
-- Table: global_superstore_orders
-- ====================================================================

DROP TABLE IF EXISTS global_superstore_orders CASCADE;

CREATE TABLE global_superstore_orders (
    row_id INT PRIMARY KEY,
    order_id VARCHAR(50) NOT NULL,
    order_date DATE NOT NULL,
    ship_date DATE NOT NULL,
    ship_mode VARCHAR(50) NOT NULL,
    customer_id VARCHAR(50) NOT NULL,
    customer_name VARCHAR(150) NOT NULL,
    segment VARCHAR(50) NOT NULL,
    city VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    postal_code VARCHAR(20) DEFAULT 'Unknown',
    market VARCHAR(50) NOT NULL,
    region VARCHAR(50) NOT NULL,
    product_id VARCHAR(50) NOT NULL,
    category VARCHAR(50) NOT NULL,
    sub_category VARCHAR(50) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    sales NUMERIC(12, 2) NOT NULL,
    quantity INT NOT NULL,
    discount NUMERIC(5, 2) NOT NULL,
    profit NUMERIC(12, 2) NOT NULL,
    shipping_cost NUMERIC(10, 2) NOT NULL,
    order_priority VARCHAR(20) NOT NULL,
    order_year INT,
    order_month INT,
    order_quarter VARCHAR(10),
    shipping_duration_days INT,
    profit_margin_pct NUMERIC(8, 2)
);

-- Recommended Indexes for High-Performance Analytical Queries
CREATE INDEX idx_orders_order_date ON global_superstore_orders (order_date);
CREATE INDEX idx_orders_customer_id ON global_superstore_orders (customer_id);
CREATE INDEX idx_orders_product_id ON global_superstore_orders (product_id);
CREATE INDEX idx_orders_category ON global_superstore_orders (category);
CREATE INDEX idx_orders_region ON global_superstore_orders (region);
CREATE INDEX idx_orders_market ON global_superstore_orders (market);
