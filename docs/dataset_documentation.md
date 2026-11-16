# Dataset Documentation: Global Superstore
**Project:** Global Retail Business Analytics & Decision Intelligence  
**Author:** Muhammad Awais Bacha | Devixo Solutions  

---

## 1. Overview & Attribution
- **Dataset Title:** Global Superstore Sales Dataset (2011–2014)
- **Primary Source:** Public benchmark dataset widely utilized in business intelligence, retail analytics, and machine learning research (Tableau Software / Kaggle).
- **Temporal Scope:** January 1, 2011 to December 31, 2014 (4 Full Fiscal Years).
- **Total Record Count:** 51,290 Transactions.
- **Total Features:** 24 Raw Columns -> 45 Cleaned and Engineered Columns.

---

## 2. Data Dictionary

| # | Attribute Name | Raw Type | Target Type | Description |
|---|----------------|----------|-------------|-------------|
| 1 | `row_id` | `int64` | `INT` | Unique record identifier |
| 2 | `order_id` | `object` | `VARCHAR` | Unique order identifier (e.g. CA-2012-124891) |
| 3 | `order_date` | `object` | `DATE` | Date when the customer placed the order |
| 4 | `ship_date` | `object` | `DATE` | Date when the order was dispatched |
| 5 | `ship_mode` | `object` | `VARCHAR` | Logistics mode (Standard Class, Second Class, First Class, Same Day) |
| 6 | `customer_id` | `object` | `VARCHAR` | Unique customer alphanumeric code |
| 7 | `customer_name` | `object` | `VARCHAR` | Full name of the customer |
| 8 | `segment` | `object` | `VARCHAR` | Market segment (Consumer, Corporate, Home Office) |
| 9 | `city` | `object` | `VARCHAR` | Destination delivery city |
| 10 | `state` | `object` | `VARCHAR` | Destination delivery state or province |
| 11 | `country` | `object` | `VARCHAR` | Destination sovereign nation (147 unique countries) |
| 12 | `postal_code` | `float64` | `VARCHAR` | Delivery postal code (US only; international = 'Unknown') |
| 13 | `market` | `object` | `VARCHAR` | Continental business market (APAC, EU, US, LATAM, Africa, EMEA, Canada) |
| 14 | `region` | `object` | `VARCHAR` | Sub-continental geographic region (13 regions) |
| 15 | `product_id` | `object` | `VARCHAR` | Unique product identifier code |
| 16 | `category` | `object` | `VARCHAR` | Primary category (Technology, Furniture, Office Supplies) |
| 17 | `sub_category` | `object` | `VARCHAR` | Secondary product classification (17 subcategories) |
| 18 | `product_name` | `object` | `VARCHAR` | Commercial title of the product |
| 19 | `sales` | `float64` | `NUMERIC` | Gross transactional sales revenue ($) |
| 20 | `quantity` | `int64` | `INT` | Total physical units purchased |
| 21 | `discount` | `float64` | `NUMERIC` | Applied promotional discount rate (0.00 to 0.85) |
| 22 | `profit` | `float64` | `NUMERIC` | Net financial profit or loss ($) |
| 23 | `shipping_cost` | `float64` | `NUMERIC` | Carrier fulfillment cost ($) |
| 24 | `order_priority`| `object` | `VARCHAR` | Operational urgency (Critical, High, Medium, Low) |
