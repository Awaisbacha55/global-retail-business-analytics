-- ====================================================================
-- Global Retail Business Analytics & Decision Intelligence
-- SQL Script: regional_analysis.sql
-- Geographic distribution, market margins, and regional growth
-- ====================================================================

-- 1. Market and Regional Performance Summary
SELECT
    market,
    region,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_profit,
    ROUND((SUM(profit) / NULLIF(SUM(sales), 0)) * 100.0, 2) AS profit_margin_pct,
    COUNT(DISTINCT order_id) AS distinct_orders,
    COUNT(DISTINCT customer_id) AS unique_customers
FROM global_superstore_orders
GROUP BY market, region
ORDER BY total_sales DESC;

-- 2. Multi-Year Regional Sales Growth
WITH regional_yearly AS (
    SELECT
        region,
        EXTRACT(YEAR FROM order_date) AS fiscal_year,
        SUM(sales) AS yearly_sales
    FROM global_superstore_orders
    GROUP BY region, EXTRACT(YEAR FROM order_date)
)
SELECT
    region,
    fiscal_year,
    ROUND(yearly_sales, 2) AS sales_amount,
    ROUND(
        ((yearly_sales - LAG(yearly_sales) OVER (PARTITION BY region ORDER BY fiscal_year)) 
        / NULLIF(LAG(yearly_sales) OVER (PARTITION BY region ORDER BY fiscal_year), 0)) * 100.0,
        2
    ) AS yoy_regional_growth_pct
FROM regional_yearly
ORDER BY region, fiscal_year;

-- 3. Top Category by Region (Using Window Function DENSE_RANK)
WITH regional_category_sales AS (
    SELECT
        region,
        category,
        ROUND(SUM(sales), 2) AS category_sales,
        ROUND(SUM(profit), 2) AS category_profit,
        DENSE_RANK() OVER (PARTITION BY region ORDER BY SUM(sales) DESC) AS rank_in_region
    FROM global_superstore_orders
    GROUP BY region, category
)
SELECT
    region,
    category AS top_category,
    category_sales,
    category_profit
FROM regional_category_sales
WHERE rank_in_region = 1
ORDER BY category_sales DESC;
