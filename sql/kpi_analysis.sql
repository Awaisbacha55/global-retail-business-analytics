-- ====================================================================
-- Global Retail Business Analytics & Decision Intelligence
-- SQL Script: kpi_queries.sql
-- Computes the seven core business KPIs matching Python implementations
-- ====================================================================

-- Master KPI Query: High-Level Overall Business Snapshot
SELECT
    ROUND(SUM(sales), 2) AS kpi_1_total_revenue,
    ROUND(SUM(profit), 2) AS kpi_2_total_profit,
    COUNT(DISTINCT order_id) AS kpi_3_total_orders,
    ROUND(SUM(sales) / NULLIF(COUNT(DISTINCT order_id), 0), 2) AS kpi_4_average_order_value,
    ROUND((SUM(profit) / NULLIF(SUM(sales), 0)) * 100.0, 2) AS kpi_5_profit_margin_pct,
    COUNT(DISTINCT customer_id) AS kpi_6_customer_count
FROM global_superstore_orders;

-- KPI 7: Year-over-Year (YoY) Growth Rates for Revenue and Profit
WITH annual_metrics AS (
    SELECT
        EXTRACT(YEAR FROM order_date) AS fiscal_year,
        ROUND(SUM(sales), 2) AS revenue,
        ROUND(SUM(profit), 2) AS profit,
        COUNT(DISTINCT order_id) AS distinct_orders,
        COUNT(DISTINCT customer_id) AS active_customers
    FROM global_superstore_orders
    GROUP BY EXTRACT(YEAR FROM order_date)
)
SELECT
    fiscal_year,
    revenue,
    profit,
    distinct_orders,
    active_customers,
    ROUND(revenue / distinct_orders, 2) AS annual_aov,
    ROUND((profit / revenue) * 100.0, 2) AS annual_margin_pct,
    ROUND(
        ((revenue - LAG(revenue) OVER (ORDER BY fiscal_year)) 
        / NULLIF(LAG(revenue) OVER (ORDER BY fiscal_year), 0)) * 100.0, 
        2
    ) AS kpi_7_revenue_growth_rate_pct,
    ROUND(
        ((profit - LAG(profit) OVER (ORDER BY fiscal_year)) 
        / NULLIF(LAG(profit) OVER (ORDER BY fiscal_year), 0)) * 100.0, 
        2
    ) AS profit_growth_rate_pct
FROM annual_metrics
ORDER BY fiscal_year;
