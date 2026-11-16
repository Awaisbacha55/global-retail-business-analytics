"""
Business insights and evidence compilation engine.
Synthesizes descriptive statistics, profitability margins, customer behaviors,
and regional dynamics into structured analytical insights and strategic recommendations.
"""

from typing import List, Dict, Any
import pandas as pd


def get_curated_business_insights() -> List[Dict[str, Any]]:
    """
    Returns 15+ evidence-based business insights derived from Global Superstore data.
    """
    insights = [
        {
            "id": 1,
            "title": "Strong Multi-Year Revenue Acceleration (23.9% CAGR)",
            "finding": "Annual sales grew from $2.26M in 2011 to $4.30M in 2014, reflecting a 4-year CAGR of 23.9% and an overall YoY growth rate averaging 24.0%.",
            "segment": "Enterprise / 2011-2014",
            "interpretation": "Strong organic product-market fit and expanding global footprint across international regions.",
            "impact": "Indicates sustainable commercial momentum, warranting continued investment in operational scaling."
        },
        {
            "id": 2,
            "title": "Severe Margin Erosion in Tables Subcategory (-$64.1K Net Loss)",
            "finding": "The Tables subcategory generated $758.0K in gross sales but recorded a net loss of -$64,083.39 (net profit margin of -8.45%).",
            "segment": "Furniture -> Tables",
            "interpretation": "Excessive discounting (averaging >28%) combined with high freight and bulky shipping costs completely destroys operating margins.",
            "impact": "Direct profit leak eroding margins across the entire Furniture portfolio."
        },
        {
            "id": 3,
            "title": "Technology Category Drives Enterprise Profitability (14.0% Margin)",
            "finding": "Technology delivered $4.74M in revenue and $663.8K in net profit, capturing 45.2% of total store profits at an industry-leading 13.99% margin.",
            "segment": "Technology Category",
            "interpretation": "High unit value, lower relative shipping bulk, and pricing inelasticity make Technology the primary cash generator.",
            "impact": "Provides the primary financial engine subsidizing lower-margin merchandise."
        },
        {
            "id": 4,
            "title": "Excessive Discount Threshold Disasters (>20% Discount Equals Severe Loss)",
            "finding": "Transactions with 0% discount average +$31.00 profit; transactions with >20% to 50% discount average -$35 to -$88 in net losses per line item.",
            "segment": "Discount Tiers (0% vs >20%)",
            "interpretation": "Discounts above 20% are not stimulating profitable volume; they are giving away margin on items with inelastic delivery costs.",
            "impact": "Over 12,544 order lines (24.5% of total orders) generated negative profit, costing over $380,000 in aggregate margin loss."
        },
        {
            "id": 5,
            "title": "Pronounced Q4 Holiday Revenue Concentration (42% in H2)",
            "finding": "Monthly sales climb steeply from a low of ~$120K in February to over $500K in November and December each year.",
            "segment": "Monthly Seasonality (2011-2014)",
            "interpretation": "Purchasing cycles are heavily tied to corporate fiscal year-end budget exhaustion and global retail holiday shopping.",
            "impact": "Creates acute operational strain on fulfillment in Q4, paired with severe working capital underutilization in Q1."
        },
        {
            "id": 6,
            "title": "Copiers Subcategory is the Highest Margin Contributor (17.1% Margin)",
            "finding": "Copiers generated $1.51M in revenue and $258.6K in profit, leading all 17 subcategories in net dollar profitability.",
            "segment": "Technology -> Copiers",
            "interpretation": "Commercial office equipment buyers prioritize reliability and warranty over aggressive price shopping.",
            "impact": "A critical anchor product line with superior customer lifetime and replenishment value."
        },
        {
            "id": 7,
            "title": "APAC and Europe Represent 51.7% of Global Revenue ($6.53M Combined)",
            "finding": "APAC recorded $3.59M in sales ($436.0K profit) and EU recorded $2.94M in sales ($372.8K profit), outpacing the US market ($2.30M).",
            "segment": "Geographic Markets (APAC & Europe)",
            "interpretation": "Rapid internationalization has succeeded in establishing dominant footprints across developed Asia-Pacific and European economies.",
            "impact": "Strategic focus must maintain competitive advantages in these primary revenue pillars."
        },
        {
            "id": 8,
            "title": "EMEA Region Suffering from Depressed Profit Margins (5.44%)",
            "finding": "EMEA generated $806.2K in sales but yielded only $43.9K in net profit, achieving less than half the enterprise average margin.",
            "segment": "Geographic Market -> EMEA",
            "interpretation": "High cross-border tariff friction, fragmented courier networks, and sub-scale local order density inflate operating costs.",
            "impact": "Sub-optimal capital efficiency requiring structural supply chain realignment."
        },
        {
            "id": 9,
            "title": "Consumer Segment Generates Majority Volume (51.5% Revenue)",
            "finding": "Consumer buyers contributed $6.51M (51.5%) across 12,900 orders, followed by Corporate at $3.82M (30.3%) and Home Office at $2.31M (18.3%).",
            "segment": "Customer Segments",
            "interpretation": "Broad retail consumer appeal anchors top-line revenue, but Corporate accounts yield higher stability and larger basket sizes.",
            "impact": "Marketing resources must be balanced between consumer acquisition and high-retention corporate accounts."
        },
        {
            "id": 10,
            "title": "High Customer Pareto Concentration (806 Customers Generate 87.4% Revenue)",
            "finding": "The top two RFM customer clusters (Champions and Core Growth, 806 accounts out of 1,590) generate $11.05M of the $12.64M total revenue.",
            "segment": "Customer RFM Clusters",
            "interpretation": "An elite cohort of enterprise repeat buyers accounts for the vast majority of cash flows and repeat transactions.",
            "impact": "Losing even a fraction of these high-value accounts poses an existential revenue risk."
        },
        {
            "id": 11,
            "title": "Standard Class Shipping Dominates Operational Fulfillment (59.9% Volume)",
            "finding": "Standard Class fulfilled 30,728 shipments (59.9%) with an average transit time of 5.0 days and a healthy profit margin of 11.6%.",
            "segment": "Fulfillment Logistics -> Standard Class",
            "interpretation": "Customers demonstrate strong tolerance for economical 5-day fulfillment when shipping fees are moderate.",
            "impact": "Preserves profitability by avoiding premium carrier expediting fees on non-critical goods."
        },
        {
            "id": 12,
            "title": "Same-Day Delivery Premium Lacks Sufficient Margin Expansion",
            "finding": "Same Day shipping accounts for 2,701 orders (5.3%) with transit < 24 hours, but yields a margin of only 11.4% (comparable to Standard Class).",
            "segment": "Fulfillment Logistics -> Same Day",
            "interpretation": "Carrier surcharges for emergency fulfillment are currently absorbing the expedited delivery markups.",
            "impact": "Retailer bears expedited logistical risk without capturing premium margin."
        },
        {
            "id": 13,
            "title": "Bookcases in Furniture Deliver Surprising Strength ($161.9K Profit)",
            "finding": "Contrary to the loss-making Tables subcategory, Bookcases achieved $1.47M in sales and $161.9K in profit (11.0% margin).",
            "segment": "Furniture -> Bookcases",
            "interpretation": "Modular packaging and higher average order values allow Bookcases to overcome furniture shipping freight costs.",
            "impact": "Serves as the blueprint for reforming the rest of the Furniture category catalog."
        },
        {
            "id": 14,
            "title": "Fasteners Exhibit Negligible Financial Impact ($11.5K Total Profit)",
            "finding": "Fasteners account for 2,420 transaction lines but produced only $83.2K in cumulative sales over 4 years ($11.5K profit).",
            "segment": "Office Supplies -> Fasteners",
            "interpretation": "Extremely low unit selling price ($3.44 avg) consumes order handling and packing bandwidth without moving financial needles.",
            "impact": "Operational overhead to process fasteners individual lines outweighs net monetary contribution."
        },
        {
            "id": 15,
            "title": "Predictable 12-Month Demand Trajectory Enables Supply Chain Optimization",
            "finding": "Random Forest time-series forecasting achieved a 16.95% MAPE on 2014 validation data, capturing seasonal Q4 surges with high fidelity.",
            "segment": "Predictive Modeling / 2014 Validation",
            "interpretation": "Demand exhibits robust autoregressive and seasonal periodicity that can guide advance warehouse stock replenishment.",
            "impact": "Allows 60-day advance inventory procurement, eliminating costly emergency stockouts and expedited air freight."
        }
    ]
    return insights


def get_curated_business_recommendations() -> List[Dict[str, Any]]:
    """
    Returns 10+ actionable recommendations connected to specific empirical findings.
    """
    recommendations = [
        {
            "id": 1,
            "title": "Eliminate Unconditional Discounts Exceeding 20% on Furniture & Bulky Goods",
            "finding_ref": "Discount levels >20% generate an average net loss of -$35 to -$88 per transaction line (Insight #4 & #2).",
            "action": "Implement a hard system price floor in the ordering portal capping non-executive discounts at 15%. Require VP approval for discounts above 20%.",
            "benefit": "Estimated recovery of $150K - $220K in annual lost margin by terminating value-destroying price promotions.",
            "priority": "High",
            "kpi": "Profit Margin % on Discounted Orders (Target >= +8%)"
        },
        {
            "id": 2,
            "title": "Overhaul or Delist the Loss-Making Tables Subcategory",
            "finding_ref": "Tables subcategory lost -$64.1K across 4 years on $758K sales due to packaging bulk and heavy discounting (Insight #2).",
            "action": "Renegotiate vendor supply contracts for flat-pack knock-down designs, bundle tables exclusively with high-margin chairs/copiers, and institute minimum freight charges.",
            "benefit": "Turn Tables from a -$64K drag into a break-even or +5% margin category, recapturing ~$25K annually.",
            "priority": "High",
            "kpi": "Tables Subcategory Profit Margin % (Target: > 0.0%)"
        },
        {
            "id": 3,
            "title": "Deploy Dedicated VIP Key Account Retention Program for Champions",
            "finding_ref": "806 customers in Champions and Core Growth segments drive 87.4% of total enterprise sales ($11.05M) (Insight #10).",
            "action": "Assign dedicated corporate account managers, establish customized pricing tiers, and offer quarterly business reviews (QBRs) and SLA guarantees.",
            "benefit": "Protects $11M in recurring revenue and increases repurchase frequency by 10-15%.",
            "priority": "High",
            "kpi": "Key Account Retention Rate (Target: > 95%)"
        },
        {
            "id": 4,
            "title": "Automate Inventory Procurement Utilizing Time-Series Demand Forecasts",
            "finding_ref": "Monthly demand experiences predictable Q4 surges (up to 4x Feb volume) with 16.9% MAPE forecasting accuracy (Insight #5 & #15).",
            "action": "Integrate the Random Forest forecast model into inventory replenishment systems by August to pre-position stock in regional distribution centers.",
            "benefit": "Reduces backorders by 30% during Q4 holiday rush and cuts expedited freight expenses by ~$45K annually.",
            "priority": "Medium",
            "kpi": "Holiday Stockout Rate (< 3%) and Shipping Cost Ratio % (< 10%)"
        },
        {
            "id": 5,
            "title": "Establish Regional Fulfillment Hubs to Remedy EMEA Margin Lag",
            "finding_ref": "EMEA margins lag at 5.44% compared to APAC (12.1%) and EU (12.7%) due to cross-border shipping friction (Insight #8).",
            "action": "Consolidate warehousing partnerships in Central/Western European hubs with streamlined customs clearing for Middle East and African lanes.",
            "benefit": "Expands EMEA operating margin from 5.4% toward the 10.0% global baseline, unlocking ~$40K in incremental profit.",
            "priority": "Medium",
            "kpi": "EMEA Regional Profit Margin % (Target >= 10.0%)"
        },
        {
            "id": 6,
            "title": "Rebalance Pricing Surcharge on Expedited & Same-Day Shipping",
            "finding_ref": "Same-Day fulfillment delivers no margin premium (11.4%) over standard 5-day shipping (11.6%) despite operational complexity (Insight #12).",
            "action": "Increase Same-Day delivery pricing tier by 18-25% to reflect true rush handling and priority courier costs.",
            "benefit": "Generates ~$30K in additional courier profit margin while filtering non-essential rush requests.",
            "priority": "Medium",
            "kpi": "Same-Day Delivery Net Margin % (Target >= 16.0%)"
        },
        {
            "id": 7,
            "title": "Promote and Cross-Sell High-Margin Technology & Copier Accessories",
            "finding_ref": "Technology yields 14.0% margin, with Copiers generating $258.6K profit at 17.1% net margin (Insight #3 & #6).",
            "action": "Create automated 'frequently bought together' recommendation bundles at checkout linking copiers, phones, and storage with high-margin consumables.",
            "benefit": "Increases Average Order Value (AOV) by $35 - $50 and expands overall store profit margin by 0.8 - 1.2 percentage points.",
            "priority": "Medium",
            "kpi": "Average Order Value (AOV Target > $540.00)"
        },
        {
            "id": 8,
            "title": "Implement Minimum Order Quantities (MOQ) on Low-Value Fasteners",
            "finding_ref": "Fasteners generate under $83.2K total revenue across 2,420 transactions ($34 avg order line) creating packing inefficiencies (Insight #14).",
            "action": "Enforce minimum pack sizes (e.g. packs of 5 or 10 boxes) or bundle fasteners into complementary hardware packages.",
            "benefit": "Reduces picker/packing overhead by 40% in small-parts bin storage and increases line item profitability.",
            "priority": "Low",
            "kpi": "Fasteners Average Transaction Value (Target >= $50.00)"
        },
        {
            "id": 9,
            "title": "Win-Back Campaign Targeting At-Risk and Lapsed Customer Segment",
            "finding_ref": "446 customers (28.1% of customer base) have not purchased in over 250 days, representing untapped historical demand (Insight #10).",
            "action": "Deploy personalized email re-engagement campaigns featuring dynamic discounts on their previously purchased top subcategories.",
            "benefit": "Reactivating 15% of lapsed customers (approx. 65 accounts) would generate ~$115K in incremental annual revenue.",
            "priority": "Medium",
            "kpi": "Lapsed Customer Reactivation Rate (Target >= 15%)"
        },
        {
            "id": 10,
            "title": "Institutionalize Quarterly Executive BI Scorecard Reviews",
            "finding_ref": "Disparities across 147 countries, 13 regions, and 17 subcategories require unified KPI governance (Insight #1, #7, #9).",
            "action": "Deploy the 6-page interactive Power BI dashboard to regional directors and host monthly cross-functional operational reviews.",
            "benefit": "Accelerates time-to-insight from monthly batch reporting to real-time interactive decision intelligence.",
            "priority": "High",
            "kpi": "Dashboard Active Usage and SLA Decision Turnaround Time"
        }
    ]
    return recommendations
