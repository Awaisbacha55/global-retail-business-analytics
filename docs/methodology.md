# Analytical Methodology & Engineering Pipeline
**Project:** Global Retail Business Analytics & Decision Intelligence  
**Author:** Muhammad Awais Bacha | Devixo Solutions Internship (Task 04)  

---

## 1. End-to-End Analytics Workflow

```
[ Raw Ingestion ] -> [ Data Quality & Cleaning ] -> [ Feature Engineering ]
                             |                              |
                             v                              v
[ SQL Architecture ] <- [ Processed Dataset (CSV) ] -> [ Machine Learning Models ]
                             |                              |
                             v                              v
                  [ Power BI Star Schema ]       [ Publication PDF Report ]
```

### Phase 1: Ingestion & Profiling
- Read raw CSV / Excel data (`Global_Superstore2.csv`) with `latin-1` encoding detection.
- Audit dimensions: 51,290 records, 24 attributes, 0 exact duplicates.
- Address missing values: identify that `Postal Code` is 80.5% missing because international orders do not record US ZIP codes; impute with `'Unknown'` and standardize US 5-digit postal codes.

### Phase 2: Feature Engineering
- Extracted temporal dimensions: `order_year`, `order_month`, `order_quarter`, `shipping_duration_days`.
- Derived financial metrics: `profit_margin_pct`, `unit_price`, `unit_cost`, `shipping_cost_ratio_pct`.
- Computed customer RFM features and order totals.

### Phase 3: Exploratory Data Analysis & Visualizations
- Created 20 high-resolution charts in `reports/figures/` analyzing sales distributions, monthly trends, subcategory margins, regional sales, and discount impact.

### Phase 4: SQL Business Intelligence
- Developed 8 PostgreSQL-compatible SQL scripts in `sql/` for data quality, sales analysis, product analysis, customer segmentation, regional breakdown, and KPI queries.
- Audited that SQL queries produce exact identical metrics to Python functions.

### Phase 5: Predictive Modeling
- **Sales Demand Forecasting:** Chronological train/test split. Random Forest model achieved 16.95% MAPE on 2014 validation hold-out, outperforming Moving Average (24.85%) and Naive (27.71%) baselines.
- **Customer RFM Segmentation:** Standardized log-transformed RFM features clustered with K-Means ($k=4$, Silhouette Score = 0.392).

### Phase 6: Reporting & BI Delivery
- Designed a 6-page interactive Power BI dashboard with Star Schema and DAX formulas.
- Generated a publication-quality 14-page PDF final report (`reports/final_project_report.pdf`).
