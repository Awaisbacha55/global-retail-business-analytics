-- ====================================================================
-- Global Retail Business Analytics & Decision Intelligence
-- SQL Script: profit_analysis.sql
-- In-depth profitability diagnostics, loss drivers, and margin erosion
-- ====================================================================

-- 1. Global Profitability and Margin Baseline
SELECT
    ROUND(SUM(profit), 2) AS total_net_profit,
    ROUND(SUM(sales), 2) AS gross_revenue,
    ROUND((SUM(profit) / NULLIF(SUM(sales), 0)) * 100.0, 2) AS overall_profit_margin_pct,
    COUNT(CASE WHEN profit < 0 THEN 1 END) AS loss_making_order_lines,
    ROUND((COUNT(CASE WHEN profit < 0 THEN 1 END)::NUMERIC / COUNT(*)) * 100.0, 2) AS loss_transaction_rate_pct
FROM global_superstore_orders;

-- 2. Top 10 Heaviest Loss-Making Products
SELECT
    product_name,
    category,
    sub_category,
    ROUND(SUM(sales), 2) AS total_sales,
    ROUND(SUM(profit), 2) AS total_net_loss,
    ROUND(AVG(discount) * 100.0, 2) AS avg_discount_pct,
    SUM(quantity) AS units_sold
FROM global_superstore_orders
GROUP BY product_name, category, sub_category
HAVING SUM(profit) < 0
ORDER BY total_net_loss ASC
LIMIT 10;

-- 3. Profitability and Margin Breakdown by Category and Segment
SELECT
    category,
    segment,
    ROUND(SUM(sales), 2) AS revenue,
    ROUND(SUM(profit), 2) AS profit,
    ROUND((SUM(profit) / NULLIF(SUM(sales), 0)) * 100.0, 2) AS margin_pct
FROM global_superstore_orders
GROUP BY category, segment
ORDER BY category, profit DESC;

-- 4. Correlation between Shipping Mode and Net Profit Margin
SELECT
    ship_mode,
    COUNT(DISTINCT order_id) AS orders_handled,
    ROUND(SUM(sales), 2) AS revenue,
    ROUND(SUM(shipping_cost), 2) AS total_shipping_cost,
    ROUND(SUM(profit), 2) AS net_profit,
    ROUND((SUM(profit) / NULLIF(SUM(sales), 0)) * 100.0, 2) AS profit_margin_pct,
    ROUND((SUM(shipping_cost) / NULLIF(SUM(sales), 0)) * 100.0, 2) AS shipping_ratio_pct
FROM global_superstore_orders
GROUP BY ship_mode
ORDER BY revenue DESC;
