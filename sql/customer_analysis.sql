-- ====================================================================
-- Global Retail Business Analytics & Decision Intelligence
-- SQL Script: customer_analysis.sql
-- Customer value contribution, loyalty tiers, and purchase frequency
-- ====================================================================

-- 1. Top 10 Customers by Lifetime Revenue
SELECT
    customer_id,
    customer_name,
    segment,
    COUNT(DISTINCT order_id) AS total_orders,
    ROUND(SUM(sales), 2) AS total_spend,
    ROUND(SUM(profit), 2) AS total_profit_generated,
    ROUND(SUM(sales) / COUNT(DISTINCT order_id), 2) AS avg_spend_per_order
FROM global_superstore_orders
GROUP BY customer_id, customer_name, segment
ORDER BY total_spend DESC
LIMIT 10;

-- 2. Customer Segmentation by Spend Tier
WITH customer_aggregates AS (
    SELECT
        customer_id,
        customer_name,
        SUM(sales) AS lifetime_spend,
        COUNT(DISTINCT order_id) AS order_count
    FROM global_superstore_orders
    GROUP BY customer_id, customer_name
)
SELECT
    CASE
        WHEN lifetime_spend >= 15000 THEN 'Tier 1: VIP Platinum ($15k+)'
        WHEN lifetime_spend >= 10000 THEN 'Tier 2: Gold ($10k - $15k)'
        WHEN lifetime_spend >= 5000  THEN 'Tier 3: Silver ($5k - $10k)'
        ELSE 'Tier 4: Bronze (< $5k)'
    END AS customer_tier,
    COUNT(*) AS customer_count,
    ROUND(SUM(lifetime_spend), 2) AS cumulative_spend,
    ROUND((SUM(lifetime_spend) / (SELECT SUM(sales) FROM global_superstore_orders)) * 100.0, 2) AS revenue_share_pct,
    ROUND(AVG(order_count), 1) AS avg_orders_per_customer
FROM customer_aggregates
GROUP BY
    CASE
        WHEN lifetime_spend >= 15000 THEN 'Tier 1: VIP Platinum ($15k+)'
        WHEN lifetime_spend >= 10000 THEN 'Tier 2: Gold ($10k - $15k)'
        WHEN lifetime_spend >= 5000  THEN 'Tier 3: Silver ($5k - $10k)'
        ELSE 'Tier 4: Bronze (< $5k)'
    END
ORDER BY cumulative_spend DESC;

-- 3. Customer Purchase Frequency Distribution
WITH customer_orders AS (
    SELECT customer_id, COUNT(DISTINCT order_id) AS orders_placed
    FROM global_superstore_orders
    GROUP BY customer_id
)
SELECT
    orders_placed,
    COUNT(*) AS number_of_customers
FROM customer_orders
GROUP BY orders_placed
ORDER BY orders_placed ASC;
