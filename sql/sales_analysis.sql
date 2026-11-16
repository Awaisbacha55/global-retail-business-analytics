-- ====================================================================
-- Global Retail Business Analytics & Decision Intelligence
-- SQL Script: sales_analysis.sql
-- Revenue trends, monthly seasonality, and multi-year growth
-- ====================================================================

-- 1. Total Global Sales and Aggregate Volume
SELECT
    ROUND(SUM(sales), 2) AS total_revenue,
    ROUND(AVG(sales), 2) AS avg_sales_per_line,
    SUM(quantity) AS total_units_sold,
    COUNT(DISTINCT order_id) AS total_orders
FROM global_superstore_orders;

-- 2. Yearly Revenue and Year-over-Year (YoY) Growth Rate
WITH yearly_sales AS (
    SELECT
        EXTRACT(YEAR FROM order_date) AS fiscal_year,
        ROUND(SUM(sales), 2) AS total_sales,
        COUNT(DISTINCT order_id) AS distinct_orders
    FROM global_superstore_orders
    GROUP BY EXTRACT(YEAR FROM order_date)
)
SELECT
    fiscal_year,
    total_sales,
    distinct_orders,
    ROUND(LAG(total_sales, 1) OVER (ORDER BY fiscal_year), 2) AS prior_year_sales,
    ROUND(
        ((total_sales - LAG(total_sales, 1) OVER (ORDER BY fiscal_year)) 
        / NULLIF(LAG(total_sales, 1) OVER (ORDER BY fiscal_year), 0)) * 100.0, 
        2
    ) AS yoy_sales_growth_pct
FROM yearly_sales
ORDER BY fiscal_year;

-- 3. Monthly Revenue Trend
SELECT
    TO_CHAR(order_date, 'YYYY-MM') AS year_month,
    ROUND(SUM(sales), 2) AS monthly_revenue,
    ROUND(SUM(profit), 2) AS monthly_profit,
    COUNT(DISTINCT order_id) AS monthly_orders
FROM global_superstore_orders
GROUP BY TO_CHAR(order_date, 'YYYY-MM')
ORDER BY year_month;

-- 4. Sales Distribution by Product Category
SELECT
    category,
    ROUND(SUM(sales), 2) AS category_revenue,
    ROUND((SUM(sales) / SUM(SUM(sales)) OVER ()) * 100.0, 2) AS revenue_share_pct,
    COUNT(DISTINCT order_id) AS order_reach
FROM global_superstore_orders
GROUP BY category
ORDER BY category_revenue DESC;

-- 5. Sales Performance Across Geographic Regions
SELECT
    region,
    market,
    ROUND(SUM(sales), 2) AS regional_revenue,
    COUNT(DISTINCT country) AS countries_served,
    COUNT(DISTINCT order_id) AS total_orders
FROM global_superstore_orders
GROUP BY region, market
ORDER BY regional_revenue DESC;
