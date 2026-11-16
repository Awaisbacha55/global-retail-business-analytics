-- ====================================================================
-- Global Retail Business Analytics & Decision Intelligence
-- SQL Script: product_analysis.sql
-- Product and catalog performance, profitability, and discount exposure
-- ====================================================================

-- 1. Top 10 Best-Selling Products by Revenue
SELECT
    product_name,
    category,
    sub_category,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    SUM(quantity) AS total_quantity_sold
FROM global_superstore_orders
GROUP BY product_name, category, sub_category
ORDER BY total_sales DESC
LIMIT 10;

-- 2. Bottom 10 Performing Products by Sales Volume
SELECT
    product_name,
    category,
    sub_category,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    SUM(quantity) AS total_quantity_sold
FROM global_superstore_orders
GROUP BY product_name, category, sub_category
ORDER BY total_sales ASC
LIMIT 10;

-- 3. Subcategory Profitability Breakdown and Margins
SELECT
    category,
    sub_category,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / NULLIF(SUM(sales), 0)) * 100.0, 2) AS profit_margin_pct,
    ROUND(AVG(discount) * 100.0, 2) AS avg_discount_pct
FROM global_superstore_orders
GROUP BY category, sub_category
ORDER BY total_profit DESC;

-- 4. Discount Impact on Product Profitability Brackets
SELECT
    CASE
        WHEN discount = 0 THEN '0% No Discount'
        WHEN discount <= 0.20 THEN '01% - 20% Low'
        WHEN discount <= 0.40 THEN '21% - 40% Medium'
        ELSE '> 40% Steep Discount'
    END AS discount_tier,
    COUNT(*) AS transaction_count,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / NULLIF(SUM(sales), 0)) * 100.0, 2) AS profit_margin_pct
FROM global_superstore_orders
GROUP BY
    CASE
        WHEN discount = 0 THEN '0% No Discount'
        WHEN discount <= 0.20 THEN '01% - 20% Low'
        WHEN discount <= 0.40 THEN '21% - 40% Medium'
        ELSE '> 40% Steep Discount'
    END
ORDER BY total_sales DESC;
