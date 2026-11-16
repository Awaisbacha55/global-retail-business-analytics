# Power BI Dashboard Implementation & Architecture Guide
**Project:** Global Retail Business Analytics & Decision Intelligence  
**Author:** Muhammad Awais Bacha | Devixo Solutions Internship  
**Task:** Task 04 — Complete Business Analytics Project  

---

## 1. Data Model Architecture (Star Schema)

The dashboard is structured on an enterprise **Star Schema** data model designed for high-performance aggregations and cross-filtering.

```
       +--------------------+
       |    Dim_Calendar    |
       +--------------------+
       | Date (PK)          |
       +---------+----------+
                 | 1
                 | 
                 | * (order_date)
+--------------------+        +--------------------+
|    Dim_Customer    |        |    Dim_Product     |
+--------------------+        +--------------------+
| customer_id (PK)   |        | product_id (PK)    |
+---------+----------+        +---------+----------+
          | 1                           | 1
          |                             | 
          | *                           | *
     +----+-----------------------------+----+
     |              Fact_Orders              |
     +---------------------------------------+
     | row_id (PK)                           |
     | order_id                              |
     | customer_id (FK)                      |
     | product_id (FK)                       |
     | order_date (FK)                       |
     | sales, profit, quantity, discount...  |
     +-------------------+-------------------+
                         | *
                         | 
                         | 1
                +--------+-----------+
                |   Dim_Geography    |
                +--------------------+
                | country, city (PK) |
                +--------------------+
```

### Table Relationships
1. **`Dim_Calendar[Date]` (1) -> `Fact_Orders[order_date]` (*)**
   - Cardinality: One to Many (1:*)
   - Cross-filter direction: Single
2. **`Dim_Customer[customer_id]` (1) -> `Fact_Orders[customer_id]` (*)**
   - Cardinality: One to Many (1:*)
   - Cross-filter direction: Single
3. **`Dim_Product[product_id]` (1) -> `Fact_Orders[product_id]` (*)**
   - Cardinality: One to Many (1:*)
   - Cross-filter direction: Single
4. **`Dim_Geography[country]` (1) -> `Fact_Orders[country]` (*)**
   - Cardinality: One to Many (1:*)
   - Cross-filter direction: Both

---

## 2. Interactive Global Slicers & Filtering Panel

Every report canvas includes a standardized top banner or expandable left drawer containing the following interactive controls:
- **Date Range Slicer:** Between slider on `Dim_Calendar[Date]` (2011-01-01 to 2014-12-31).
- **Fiscal Year Dropdown:** `Dim_Calendar[Year]` (Multi-select enabled: 2011, 2012, 2013, 2014).
- **Market & Region Dropdown:** `Dim_Geography[market]` hierarchy drilling down to `region`.
- **Product Category Pill:** `Dim_Product[category]` (Technology, Furniture, Office Supplies).
- **Customer Segment Selector:** `Dim_Customer[segment]` (Consumer, Corporate, Home Office).

---

## 3. Page-by-Page Visual Specification

### Page 1: Executive Summary
*Objective:* High-altitude strategic view of enterprise health, scale, and multi-year trajectory.
* **Top KPI Scorecards (Cards):**
  - Total Revenue: `$12.64M`
  - Total Profit: `$1.47M`
  - Total Orders: `25,035`
  - Average Order Value: `$504.99`
  - Net Profit Margin: `11.61%`
  - Total Active Customers: `1,590`
  - 4-Year Revenue CAGR: `+23.9%`
* **Visual 1 (Area / Line Chart):** 48-Month Revenue and Profit Trend with dynamic anomaly callouts.
* **Visual 2 (Clustered Column Chart):** Annual Revenue by Category with YoY growth rate tags.
* **Visual 3 (Donut Chart):** Customer Segment Contribution (`Consumer: 51.5%`, `Corporate: 30.3%`, `Home Office: 18.2%`).

### Page 2: Sales Analysis
*Objective:* Comprehensive examination of revenue velocity, seasonality, and product demand.
* **Visual 1 (Line & Stacked Column Chart):** Monthly Sales vs Monthly Order Volume (highlighting Q4 peak seasonality).
* **Visual 2 (Waterfall Chart):** Yearly Revenue bridge showing growth contribution by Category.
* **Visual 3 (Horizontal Bar Chart):** Subcategory Revenue ranking with 80/20 cumulative Pareto overlay.
* **Visual 4 (Matrix Table):** Quarter vs Category Sales with conditional data bars.

### Page 3: Product Analysis
*Objective:* Catalog rationalization, top performers, and portfolio health.
* **Visual 1 (Bar Chart):** Top 10 Revenue Generators (led by Canon ImageCLASS Copier, Apple Smart Phone).
* **Visual 2 (Bar Chart):** Bottom 10 Revenue Items (slow-moving inventory flags).
* **Visual 3 (Scatter Plot):** Subcategory Matrix (Sales vs Profit Margin % with bubble size as Units Sold).
* **Visual 4 (Tree Map):** Hierarchical view of Category -> Subcategory -> Total Sales.

### Page 4: Customer Analysis
*Objective:* Customer lifetime value, repeat purchasing patterns, and segmentation.
* **Visual 1 (Table Visual):** Top 10 VIP Customers by spend, average order size, and lifetime profit.
* **Visual 2 (Histogram):** Customer Order Frequency Distribution (1 to 37 orders per customer).
* **Visual 3 (Clustered Bar Chart):** Revenue and Profit Contribution across RFM Segments (Champions, Core, Occasional, At-Risk).
* **Visual 4 (Scatter Plot):** Recency vs Monetary Value per customer.

### Page 5: Regional Analysis
*Objective:* Geographic footprint, regional growth velocity, and market penetration.
* **Visual 1 (Filled Map / Shape Map):** Global Sales by Country (147 countries shaded by revenue density).
* **Visual 2 (Clustered Bar Chart):** Sales and Profit by Region (APAC, EU, US, LATAM, etc.).
* **Visual 3 (Matrix Grid):** Region vs Category profitability with color heat scale.
* **Visual 4 (Decomposition Tree):** Root: Total Revenue -> Market -> Region -> Country -> Category.

### Page 6: Profit Analysis & Risk Diagnostics
*Objective:* Profit leaks, discount margin erosion, and fulfillment cost burdens.
* **Visual 1 (Clustered Column Chart):** Average Profit per Order Line across Discount Brackets (revealing steep losses beyond 20% discount).
* **Visual 2 (Table Visual):** Top 10 Heaviest Loss-Making Products with average discount rates.
* **Visual 3 (Scatter Plot):** Order Line Sales vs Profit colored by Profitability Status.
* **Visual 4 (Bar Chart):** Net Profit Margin by Shipping Mode (Standard, Second, First, Same Day).

---

## 4. Manual Construction Steps in Power BI Desktop

1. **Launch Power BI Desktop** -> Click **Get Data** -> **Text/CSV**.
2. Navigate to `dashboard/exports/` and import:
   - `Dim_Calendar.csv`
   - `Dim_Customer.csv`
   - `Dim_Product.csv`
   - `Dim_Geography.csv`
   - `Fact_Orders.csv`
3. In **Model View**, verify relationships match the Star Schema diagram above. Ensure all foreign key data types match primary keys.
4. Create a dedicated table named `_Measures` using **Enter Data**.
5. Copy each DAX formula from `dashboard/dax_measures.md` into the `_Measures` table.
6. Build pages 1 through 6 following the visual specs and styling guidelines.
7. Format theme colors: Primary (`#1f77b4`), Accent Green (`#2ca02c`), Alert Red (`#d62728`).
8. Save as `dashboard/powerbi/Global_Retail_Analytics.pbix`.
