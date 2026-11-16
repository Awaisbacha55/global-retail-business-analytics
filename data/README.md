# Dataset Information & Setup Guide
**Project:** Global Retail Business Analytics & Decision Intelligence  
**Author:** Muhammad Awais Bacha | Devixo Solutions Internship  

---

## 1. Dataset Overview

This repository utilizes the **Global Superstore** commercial retail dataset (2011–2014), a standard enterprise benchmark dataset widely recognized across data science and business intelligence disciplines.

- **Primary Temporal Range:** January 1, 2011 – December 31, 2014 (48 Months)
- **Total Records:** 51,290 Transactions
- **Raw Features:** 24 Columns
- **Engineered Features:** 21 Columns (45 Columns Total in Processed Dataset)
- **Geographic Coverage:** 147 Sovereign Nations, 13 Geographic Regions, 7 Continental Markets

---

## 2. Directory Structure

```
data/
├── raw/
│   ├── Global_Superstore2.csv       # Original raw transaction records (12 MB)
│   └── Global_Superstore2.xlsx      # Original raw Excel workbook (8 MB)
│
├── processed/
│   └── cleaned_global_superstore.csv # Cleaned & feature-engineered dataset (45 cols)
│
└── README.md                         # This dataset documentation
```

---

## 3. Data Ingestion & Regeneration Instructions

If you need to re-run the entire data preparation, cleaning, and feature engineering pipeline:

```bash
# Run data preparation pipeline from project root
python -m src.data.prepare_data
```

This will automatically:
1. Ingest `data/raw/Global_Superstore2.csv`
2. Standardize column names to lower `snake_case`
3. Parse `order_date` and `ship_date` with `dayfirst=True`
4. Standardize US 5-digit postal codes and label non-US postal codes as `'Unknown'`
5. Engineer 21 temporal, financial, margin, and RFM features
6. Output `data/processed/cleaned_global_superstore.csv` and `dashboard/exports/powerbi_superstore_model.csv`
