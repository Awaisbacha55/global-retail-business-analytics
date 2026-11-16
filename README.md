# Global Retail Business Analytics & Decision Intelligence
### End-to-End Enterprise Analytics, PostgreSQL Architecture, Power BI Modeling & Machine Learning

**Student Name:** Muhammad Awais Bacha  
**Internship Organization:** Devixo Solutions  
**Task Number:** Task 04 — Complete Business Analytics Project  
**Repository Name:** `global-retail-business-analytics`  
**License:** Open Academic & Portfolio License  

---

## 1. Executive Summary & Project Overview

This project delivers a complete enterprise decision intelligence solution built upon **51,290 commercial transactions** across **147 countries** from the **Global Superstore** commercial retail dataset (2011–2014).

The solution integrates:
- Automated data ingestion, cleaning, and domain feature engineering (21 new features)
- Exploratory data analysis generating 20 publication-quality analytical visualizations
- Mathematical derivation and SQL validation of 7 core executive KPIs
- PostgreSQL-compatible SQL database architecture across 8 production-grade scripts
- Enterprise Star Schema data modeling and complete DAX measures for a 6-page Power BI dashboard
- Predictive time-series sales forecasting (Random Forest with 16.95% MAPE)
- Customer lifetime RFM segmentation via K-Means clustering ($k=4$, Silhouette Score: 0.392)
- 15 evidence-based business insights and 10 prioritized strategic recommendations
- An automated 14-page publication-quality executive PDF report (`reports/final_project_report.pdf`)

---

## 2. Core Executive KPIs (Audited)

All metrics were computed in Python and verified to match identical PostgreSQL / SQL calculations to the exact cent:

| KPI # | Executive Metric | Mathematical Formulation | Empirical Result |
|:-----:|------------------|--------------------------|:----------------:|
| **1** | **Total Revenue** | $\sum \text{Sales}$ | **$12,642,501.91** |
| **2** | **Total Net Profit** | $\sum \text{Profit}$ | **$1,467,457.29** |
| **3** | **Total Orders** | $\text{Distinct Count}(\text{Order ID})$ | **25,035** |
| **4** | **Average Order Value (AOV)** | $\frac{\text{Total Revenue}}{\text{Total Orders}}$ | **$504.99** |
| **5** | **Net Profit Margin %** | $\left(\frac{\text{Total Profit}}{\text{Total Revenue}}\right) \times 100$ | **11.61%** |
| **6** | **Active Customer Base** | $\text{Distinct Count}(\text{Customer ID})$ | **1,590** |
| **7** | **4-Year Sales Growth (CAGR)**| $\left(\sqrt[3]{\frac{\text{Sales}_{2014}}{\text{Sales}_{2011}}} - 1\right) \times 100$ | **+23.93%** |

---

## 3. Technology Stack & Environment

- **Core Analytics & Data Prep:** Python 3.12+ / 3.14+, Pandas 2.2+, NumPy 1.26+
- **Machine Learning & Modeling:** Scikit-Learn 1.4+, SciPy 1.12+
- **Visual Analytics:** Matplotlib 3.8+, Seaborn 0.13+
- **Document & PDF Compilation:** ReportLab 4.1+, OpenPyXL 3.1+
- **Testing & Quality Assurance:** Pytest 8.0+
- **Database & SQL:** PostgreSQL 17 / SQLite 3.50+ (CTEs, Window Functions, Aggregations)
- **Business Intelligence:** Microsoft Power BI (Star Schema, DAX Time Intelligence)

---

## 4. Repository Structure

```
global-retail-business-analytics/
├── data/
│   ├── raw/                              # Original Global Superstore dataset (CSV & XLSX)
│   ├── processed/                        # Cleaned dataset with 45 attributes
│   └── external/                         # External reference datasets
├── notebooks/                            # 6 Interactive Jupyter Notebooks
│   ├── 01_dataset_inspection.ipynb
│   ├── 02_data_cleaning.ipynb
│   ├── 03_feature_engineering.ipynb
│   ├── 04_exploratory_data_analysis.ipynb
│   ├── 05_business_analysis.ipynb
│   └── 06_machine_learning.ipynb
├── src/                                  # Modular, tested Python source code
│   ├── data/                             # Ingestion, cleaning, and preparation
│   ├── analysis/                         # KPI calculation and insight engines
│   ├── visualization/                    # Visualization and PDF generators
│   └── models/                           # Forecasting and clustering algorithms
├── sql/                                  # 8 PostgreSQL analytical scripts
│   ├── schema.sql
│   ├── data_quality_checks.sql
│   ├── sales_analysis.sql
│   ├── product_analysis.sql
│   ├── customer_analysis.sql
│   ├── regional_analysis.sql
│   ├── profit_analysis.sql
│   └── kpi_queries.sql
├── dashboard/                            # Power BI BI assets
│   ├── powerbi/                          # PBIX project models
│   ├── exports/                          # Star Schema dimension & fact tables
│   ├── dax_measures.md                   # Complete verified DAX measures
│   └── dashboard_guide.md                # 6-page dashboard build specification
├── reports/                              # Deliverables and figures
│   ├── figures/                          # 20 high-resolution analytical figures
│   ├── data_quality_report.md
│   ├── business_analytics_report.md
│   ├── executive_summary.md
│   ├── insights_and_recommendations.md
│   └── final_project_report.pdf          # Final 14-page executive PDF report
├── models/                               # Serialized models and plots
│   ├── sales_forecasting/
│   └── customer_segmentation/
├── tests/                                # Automated Pytest test suite (11 tests)
│   ├── test_data_cleaning.py
│   ├── test_kpis.py
│   └── test_data_integrity.py
├── docs/                                 # Architectural & dataset documentation
├── main.py                               # Master end-to-end execution pipeline
├── requirements.txt                      # Python dependencies
├── config.py                             # Configuration and path settings
├── LICENSE                               # Project license
└── README.md                             # Project presentation
```

---

## 5. Machine Learning Highlights

### Model A: Time-Series Sales Demand Forecasting
- **Methodology:** Chronological split (Training: 2012–2013, Holdout Validation: 2014 full year).
- **Architecture:** Random Forest Regressor leveraging calendar indices, lags (1, 2, 3, 12 months), and rolling moving averages (3, 6 months).
- **Evaluation vs Baselines (Test Set $n=12$):**
  - **Random Forest Model:** **MAE: $68,184.35 | RMSE: $85,070.62 | MAPE: 16.95%**
  - **3-Month Moving Average Baseline:** MAE: $78,159.80 | RMSE: $93,846.43 | MAPE: 24.85%
  - **Naive Lag-1 Baseline:** MAE: $90,570.82 | RMSE: $106,287.21 | MAPE: 27.71%
- **Strategic Impact:** Captured seasonal Q4 surges with high fidelity, enabling 90-day forward procurement to prevent holiday stockouts.

### Model B: Customer RFM Segmentation
- **Methodology:** Recency, Frequency, and Monetary (RFM) extraction, log-normalized and standardized, clustered via K-Means ($k=4$, Silhouette Score: 0.392).
- **Segment Breakdown:**
  1. **Champions (High-Value Loyal):** 288 accounts | Avg Spend: $14,186.62 | 32.32% Revenue Share
  2. **Core Growth Customers:** 518 accounts | Avg Spend: $13,444.02 | 55.08% Revenue Share
  3. **Occasional Shoppers:** 338 accounts | Avg Spend: $2,365.26 | 6.32% Revenue Share
  4. **At-Risk / Lapsed:** 446 accounts | Avg Spend: $1,778.70 | 6.27% Revenue Share
- **Strategic Finding:** Just 806 accounts (Champions + Core Growth) account for **87.4% ($11.05M)** of total enterprise revenue.

---

## 6. Top Strategic Business Insights

1. **Double-Digit Growth Trajectory:** Annual sales expanded from $2.26M (2011) to $4.30M (2014) at an annualized 23.9% CAGR.
2. **Technology Drives Profitability:** Technology generated $4.74M in sales and $663.8K in net profit (45.2% of store profits) at a 14.0% margin. Copiers alone delivered $258.6K in profit (17.1% margin).
3. **The Tables Subcategory Loss Drain:** The Tables subcategory generated $758.0K in sales but lost -$64,083.39 (-8.45% margin) due to packaging bulk and excessive discounting.
4. **Discounts Above 20% Destroy Margins:** Over 12,544 lines (24.5%) incurred net losses, totaling >$380,000 in lost margin. Discounts >20% average -$35 to -$88 in net loss per order line.
5. **APAC & Europe Drive 51.7% of Global Sales:** APAC ($3.59M) and Europe ($2.94M) outpaced the domestic US market ($2.30M), representing the enterprise's primary revenue pillars.

---

## 7. Priority Strategic Recommendations

| # | Recommendation | Target Impact | Priority | Target KPI |
|---|----------------|---------------|:--------:|------------|
| 1 | **Institute 20% Discount Hard Ceiling** | Recover $150K–$220K in annual lost margin | **High** | Discounted Order Margin (>= +8%) |
| 2 | **Restructure Tables Catalog** | Turn -$64.1K loss into break-even/profit | **High** | Tables Profit Margin % (> 0.0%) |
| 3 | **Launch VIP Retention Program for Champions** | Protect $11M in core recurring revenue | **High** | Key Account Retention (>= 95%) |
| 4 | **Embed ML Forecast into Procurement** | Cut Q4 stockouts by 30% and rush freight by $45K | **Medium** | Stockout Rate (< 3%) |
| 5 | **Establish Centralized EMEA Logistics Hub** | Elevate EMEA margin from 5.4% toward 10.0% | **Medium** | EMEA Profit Margin % (>= 10.0%) |

---

## 8. Installation & Execution Guide

### Prerequisites
- Python 3.12+ or 3.14+ installed.
- Git installed.

### Setup Instructions
```bash
# 1. Clone or navigate to the repository
cd "global-retail-business-analytics"

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run automated test suite
pytest tests/

# 4. Execute the complete end-to-end pipeline
python main.py
```

### Generated Deliverables
- Processed Dataset: `data/processed/cleaned_global_superstore.csv`
- Power BI Star Schema: `dashboard/exports/`
- Analytical Figures: `reports/figures/` (20 figures)
- Final PDF Report: `reports/final_project_report.pdf` (14 pages)

---

## 9. Author & Attribution

- **Author:** Muhammad Awais Bacha
- **Internship Organization:** Devixo Solutions
- **Project Track:** Data Science Internship — Task 04
- **Dataset Attribution:** Global Superstore public retail analytics benchmark dataset (Tableau / Kaggle).
