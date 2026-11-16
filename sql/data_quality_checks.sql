-- ====================================================================
-- Global Retail Business Analytics & Decision Intelligence
-- SQL Script: data_quality_checks.sql
-- Performs foundational audits on missing values, duplicates, and anomalies
-- ====================================================================

-- 1. Check Total Row Count
SELECT COUNT(*) AS total_records
FROM global_superstore_orders;

-- 2. Audit Missing Values in Critical Columns
SELECT
    SUM(CASE WHEN row_id IS NULL THEN 1 ELSE 0 END) AS null_row_id,
    SUM(CASE WHEN order_id IS NULL THEN 1 ELSE 0 END) AS null_order_id,
    SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) AS null_customer_id,
    SUM(CASE WHEN product_id IS NULL THEN 1 ELSE 0 END) AS null_product_id,
    SUM(CASE WHEN sales IS NULL THEN 1 ELSE 0 END) AS null_sales,
    SUM(CASE WHEN profit IS NULL THEN 1 ELSE 0 END) AS null_profit,
    SUM(CASE WHEN postal_code IS NULL OR postal_code = 'Unknown' THEN 1 ELSE 0 END) AS unpopulated_postal_codes
FROM global_superstore_orders;

-- 3. Duplicate Order Line Detection
SELECT row_id, COUNT(*) AS occurrence_count
FROM global_superstore_orders
GROUP BY row_id
HAVING COUNT(*) > 1;

-- 4. Date Logic Validation (Ship Date prior to Order Date)
SELECT order_id, order_date, ship_date
FROM global_superstore_orders
WHERE ship_date < order_date;

-- 5. Negative Sales or Quantity Anomalies
SELECT
    COUNT(CASE WHEN sales < 0 THEN 1 END) AS negative_sales_count,
    COUNT(CASE WHEN quantity <= 0 THEN 1 END) AS invalid_quantity_count,
    COUNT(CASE WHEN discount < 0 OR discount > 1 THEN 1 END) AS invalid_discount_count
FROM global_superstore_orders;
