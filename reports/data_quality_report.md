# Data Quality & Profiling Report
**Project:** Global Retail Business Analytics & Decision Intelligence  
**Author:** Muhammad Awais Bacha | Devixo Solutions Internship  
**Task:** Task 04 — Complete Business Analytics Project  
**Date:** November 2026  

---

## 1. Executive Summary of Dataset Health

The Global Superstore dataset was thoroughly evaluated for structural completeness, numerical validity, duplicate integrity, and temporal sequence consistency.

| Quality Dimension | Assessment Metric | Status | Resolution / Action Taken |
|-------------------|-------------------|:------:|---------------------------|
| **Row Count** | 51,290 Transactions | PASS | Complete historical scope intact (2011–2014) |
| **Column Count** | 24 Raw -> 45 Engineered | PASS | 21 analytical features added |
| **Duplicate Records** | 0 Exact Duplicate Rows | PASS | No deduplication filtering necessary |
| **Missing Values** | `Postal Code` (41,296 nulls) | PASS | Handled: Standardized US ZIPs, classified international as 'Unknown' |
| **Date Validity** | 51,290 Valid Chronological Pairs | PASS | Dayfirst=True parsing; verified `ship_date` >= `order_date` |
| **Financial Boundaries** | Sales > 0, Quantity > 0 | PASS | Confirmed no corrupted zero or negative sales records |
| **Outlier Assessment** | High-value B2B transactions | PASS | Retained legitimate enterprise bulk orders |

---

## 2. In-Depth Missing Value Treatment

### The Postal Code Analysis
- **Finding:** In the raw dataset, 41,296 records (80.52%) lacked a value for `Postal Code`.
- **Root Cause Investigation:** A geographic cross-tabulation revealed that `Postal Code` was populated exclusively for orders in the **United States** market (9,994 populated US records). International transactions across the remaining 146 countries (e.g., APAC, Europe, LATAM, Africa) do not utilize US-style 5-digit ZIP codes in this data collection.
- **Methodology & Decision:**
  - Deleting records with missing postal codes would have eliminated 80.5% of the entire global business, destroying valid sales in major markets.
  - Imputing numeric values (such as zero or the mean) would introduce false geospatial coordinates.
  - **Resolution Applied:** Retained all valid US postal codes formatted as 5-digit zero-padded strings, and cleanly assigned `'Unknown'` to all international records.

---

## 3. Outlier and Statistical Distribution Analysis

Statistical outlier detection was performed across the core numerical fields using the Interquartile Range (IQR) technique ($Q_1 - 1.5 \times IQR$ to $Q_3 + 1.5 \times IQR$).

| Feature | Min | Q1 (25%) | Median (50%) | Q3 (75%) | Max | IQR | Outliers Count | Action & Justification |
|---------|-----|----------|--------------|----------|-----|-----|:--------------:|------------------------|
| **Sales ($)** | 0.44 | 30.76 | 85.05 | 251.05 | 22,638.48 | 220.29 | 5,655 | **Retained**: High-value technology/office equipment orders represent genuine enterprise B2B sales |
| **Profit ($)** | -6,599.98 | 0.00 | 9.24 | 36.81 | 8,399.98 | 36.81 | 9,765 | **Retained**: Negative profits reflect severe discounting; extreme positive profits reflect high-margin equipment |
| **Quantity** | 1 | 2 | 3 | 5 | 14 | 3 | 877 | **Retained**: Legitimate bulk commercial office orders |
| **Discount** | 0.00 | 0.00 | 0.00 | 0.20 | 0.85 | 0.20 | 2,171 | **Retained**: Reflects heavy clearance pricing and promotion policies |
| **Shipping Cost ($)**| 0.002 | 2.61 | 7.79 | 24.45 | 933.57 | 21.84 | 5,913 | **Retained**: High costs correspond directly to international rush air cargo |

**Business Decision on Outliers:**  
Automatic truncation or removal of high-value business transactions would severely distort total revenue and profit totals. These data points represent valid enterprise behavior rather than sensor noise or entry error.

---

## 4. Chronological and Temporal Integrity

- **Minimum Order Date:** January 1, 2011  
- **Maximum Order Date:** December 31, 2014  
- **Fulfillment Duration:**
  - Minimum Shipping Time: 0 days (Same Day service)
  - Maximum Shipping Time: 7 days
  - Mean Shipping Time: 3.97 days
  - Standard Deviation: 1.75 days
- All transactions satisfied `order_date <= ship_date`. No impossible temporal anomalies were detected.
