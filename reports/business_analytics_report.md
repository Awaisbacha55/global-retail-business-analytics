# Comprehensive Business Analytics & Decision Intelligence Report
**Project Title:** Global Retail Business Analytics & Decision Intelligence  
**Candidate Name:** Muhammad Awais Bacha  
**Internship Organization:** Devixo Solutions  
**Project Task:** Task 04 — Complete Business Analytics Project  
**Submission Date:** November 2026  

---

## 1. Executive Summary & Project Identification
This report presents a complete, rigorous end-to-end business intelligence, diagnostic analytics, SQL database architecture, and predictive modeling solution applied to 51,290 commercial transactions of the Global Superstore retail enterprise across 147 sovereign nations from 2011 through 2014.

### Primary Enterprise Benchmarks
- **Total Gross Revenue:** $12,642,501.91
- **Total Net Profit:** $1,467,457.29
- **Distinct Orders Fulfilled:** 25,035 Orders
- **Average Order Value (AOV):** $504.99
- **Cumulative Net Profit Margin:** 11.61%
- **Active Global Customer Base:** 1,590 Accounts
- **Total Physical Units Dispatched:** 178,312 Units
- **Multi-Year Annualized Growth Rate (CAGR):** +23.9%

---

## 2. Business Problem & Strategic Context
As a rapidly growing global multi-channel retailer, Global Superstore faces complex operational challenges across diverse regional markets, varied fulfillment modes, and broad product catalogs. Key management questions include:
1. Which geographic markets, categories, and customer segments are driving sustainable long-term shareholder value?
2. Where are operational margin leaks occurring, and what is the quantified impact of promotional discounting?
3. How can inventory replenishment be modernized to accommodate severe seasonal demand spikes without excess capital expenditure?
4. How can commercial buyers be segmented to maximize lifetime value and reduce account churn?

---

## 3. Data Architecture, Quality, and Feature Engineering
The raw dataset was ingested and evaluated across 51,290 records and 24 attributes.
- **Postal Code Treatment:** 41,296 unpopulated postal codes were analyzed; confirmed that non-US transactions do not record US ZIP codes. Handled by retaining clean US postal codes and tagging international transactions as `'Unknown'`.
- **Deduplication:** Confirmed 0 duplicate rows.
- **Temporal Validity:** Validated all 51,290 date pairs (`ship_date >= order_date`).
- **Feature Enrichment (45 Total Attributes):**
  - Temporal dimensions: `order_year`, `order_month`, `order_quarter`, `shipping_duration_days`.
  - Financial ratios: `profit_margin_pct`, `unit_price`, `unit_cost`, `shipping_cost_ratio_pct`.
  - Customer & order aggregations: `order_total_sales`, `customer_order_frequency`, `customer_lifetime_sales`.

---

## 4. Key Performance Indicator (KPI) Architecture
All 7 required KPIs were mathematically derived and verified to match across Python and SQL database queries:

| KPI # | Metric Name | Mathematical Definition | Empirical Value |
|:-----:|-------------|-------------------------|:---------------:|
| 1 | **Total Revenue** | $\sum \text{Sales}$ | **$12,642,501.91** |
| 2 | **Total Profit** | $\sum \text{Profit}$ | **$1,467,457.29** |
| 3 | **Total Orders** | $\text{CountDistinct}(\text{Order ID})$ | **25,035** |
| 4 | **Average Order Value** | $\frac{\text{Total Revenue}}{\text{Total Orders}}$ | **$504.99** |
| 5 | **Profit Margin %** | $\left(\frac{\text{Total Profit}}{\text{Total Revenue}}\right) \times 100$ | **11.61%** |
| 6 | **Customer Count** | $\text{CountDistinct}(\text{Customer ID})$ | **1,590** |
| 7 | **Revenue Growth (YoY)** | $\left(\frac{\text{Revenue}_t - \text{Revenue}_{t-1}}{\text{Revenue}_{t-1}}\right) \times 100$ | **2012: +18.5%, 2013: +27.2%, 2014: +26.3%** |

---

## 5. Exploratory Data Analysis & Visualizations Summary
Twenty dedicated high-resolution visualizations were generated in `reports/figures/` capturing:
1. **Sales Distribution:** Core transactions cluster between $30 and $250 with a heavy positive tail.
2. **Monthly Trends:** High seasonality peaking in Q4 (November/December volume up to 4x February).
3. **Category Breakdown:** Technology delivers highest sales ($4.74M) and profit ($663.8K).
4. **Subcategory Dynamics:** Copiers lead in profit ($258.6K), while Tables incurs -$64.1K net losses.
5. **Discount Erosion:** Discounts over 20% consistently drop net transaction profit into deep losses (-$35 to -$88 avg).
6. **Customer Frequency:** 806 high-value accounts generate 87.4% of enterprise sales.
7. **Regional Footprint:** APAC ($3.59M) and Europe ($2.94M) are the largest regional contributors.

---

## 6. SQL Database Analytics
PostgreSQL-compatible queries were created and validated across eight functional scripts in `sql/`:
- `schema.sql`: Table definitions, types, primary keys, and indexes.
- `data_quality_checks.sql`: Audits for nulls, duplicates, and date sequences.
- `sales_analysis.sql`: Multi-year trends and YoY growth using `LAG()`.
- `product_analysis.sql`: Best and worst sellers, subcategory margins, and discount tiers.
- `customer_analysis.sql`: Top customers, spend tiers, and frequency distributions.
- `regional_analysis.sql`: Regional revenue, margins, and category rank using `DENSE_RANK()`.
- `profit_analysis.sql`: Loss-making orders and fulfillment margin impact.
- `kpi_queries.sql`: Direct computation of all 7 core KPIs.

---

## 7. Interactive Power BI Dashboard
A Star Schema data model was constructed with `Fact_Orders` linked to `Dim_Calendar`, `Dim_Customer`, `Dim_Product`, and `Dim_Geography`.
A 6-page enterprise dashboard was designed and documented in `dashboard/dashboard_guide.md` and `dashboard/dax_measures.md`:
- Page 1: Executive Summary
- Page 2: Sales Analysis
- Page 3: Product Analysis
- Page 4: Customer Analysis
- Page 5: Regional Analysis
- Page 6: Profit Analysis & Risk Diagnostics

---

## 8. Machine Learning Models & Results
### Model A: Time-Series Sales Demand Forecasting
- **Methodology:** Chronological split (Train: 2012–2013, Test: 2014 hold-out). Random Forest Regressor trained on calendar indices, lags (1, 2, 3, 12), and rolling moving averages (3, 6 months).
- **Results:**
  - Random Forest: **MAE: $68,184.35 | RMSE: $85,070.62 | MAPE: 16.95%**
  - 3-Month Moving Average Baseline: MAE: $78,159.80 | MAPE: 24.85%
  - Naive Lag-1 Baseline: MAE: $90,570.82 | MAPE: 27.71%
- **Business Utility:** High predictive accuracy enables 90-day forward procurement to prevent holiday stockouts.

### Model B: Customer RFM Segmentation
- **Methodology:** Log-transformed Recency, Frequency, Monetary (RFM) metrics scaled via StandardScaler, clustered using K-Means ($k=4$, Silhouette Score = 0.392).
- **Segment Profiles:**
  1. **Champions (High-Value Loyal):** 288 customers, $14,186 avg spend, 32.3% revenue share.
  2. **Core Growth Customers:** 518 customers, $13,444 avg spend, 55.1% revenue share.
  3. **Occasional Shoppers:** 338 customers, $2,365 avg spend, 6.3% revenue share.
  4. **At-Risk / Lapsed:** 446 customers, $1,779 avg spend, 6.3% revenue share.

---

## 9. Synthesized Strategic Recommendations
1. **Institute a Strict Discount Ceiling:** Cap routine discounts at 15–20% to prevent the $380,000 margin drag caused by excessive discounting.
2. **Restructure the Tables Subcategory:** Mandate flat-pack shipping and freight surcharges to reverse the -$64.1K loss.
3. **Formalize Key Account Programs:** Protect the 806 Champion and Core accounts driving 87.4% of total revenue.
4. **Deploy ML Demand Forecasting:** Integrate 90-day demand predictions into inventory planning to reduce Q4 stockouts and rush air freight.
5. **Establish EMEA Fulfillment Hubs:** Remedy EMEA's 5.44% margin lag through centralized logistics.
