# Power BI DAX Measures Reference
**Project:** Global Retail Business Analytics & Decision Intelligence  
**Author:** Muhammad Awais Bacha | Devixo Solutions Internship (Task 04)  
**Model Architecture:** Star Schema (`Fact_Orders`, `Dim_Calendar`, `Dim_Customer`, `Dim_Product`, `Dim_Geography`)

---

## 1. Core Financial & Volume Measures

### Total Revenue
```dax
Total Revenue = 
SUM(Fact_Orders[sales])
```
*Format:* Currency (`$#,##0.00`), Data Type: Decimal Number  
*Description:* Sum of all gross transactional sales across order lines.

### Total Profit
```dax
Total Profit = 
SUM(Fact_Orders[profit])
```
*Format:* Currency (`$#,##0.00`), Data Type: Decimal Number  
*Description:* Sum of all net profits (and losses) across transactions.

### Total Orders
```dax
Total Orders = 
DISTINCTCOUNT(Fact_Orders[order_id])
```
*Format:* Whole Number (`#,##0`)  
*Description:* Distinct count of unique customer orders placed.

### Total Units Sold
```dax
Total Units Sold = 
SUM(Fact_Orders[quantity])
```
*Format:* Whole Number (`#,##0`)  
*Description:* Total physical quantity of products fulfilled.

### Total Shipping Cost
```dax
Total Shipping Cost = 
SUM(Fact_Orders[shipping_cost])
```
*Format:* Currency (`$#,##0.00`)  
*Description:* Cumulative logistics and fulfillment expenses.

### Customer Count
```dax
Customer Count = 
DISTINCTCOUNT(Fact_Orders[customer_id])
```
*Format:* Whole Number (`#,##0`)  
*Description:* Distinct active customer accounts.

---

## 2. Executive Performance & Ratio Measures

### Average Order Value (AOV)
```dax
Average Order Value = 
DIVIDE([Total Revenue], [Total Orders], 0)
```
*Format:* Currency (`$#,##0.00`)  
*Description:* Mean gross revenue generated per completed order.

### Profit Margin %
```dax
Profit Margin % = 
DIVIDE([Total Profit], [Total Revenue], 0)
```
*Format:* Percentage (`0.00%`)  
*Description:* Percentage of total revenue retained as net profit.

### Shipping Cost Ratio %
```dax
Shipping Cost Ratio % = 
DIVIDE([Total Shipping Cost], [Total Revenue], 0)
```
*Format:* Percentage (`0.00%`)  
*Description:* Operational logistics burden as a fraction of gross sales.

### Average Discount %
```dax
Average Discount % = 
AVERAGE(Fact_Orders[discount])
```
*Format:* Percentage (`0.00%`)  
*Description:* Arithmetic mean discount rate applied across item lines.

---

## 3. Time Intelligence & Growth Measures

### Revenue Prior Year (PY)
```dax
Revenue Prior Year = 
CALCULATE(
    [Total Revenue],
    SAMEPERIODLASTYEAR(Dim_Calendar[Date])
)
```

### YoY Revenue Growth %
```dax
YoY Revenue Growth % = 
VAR PriorRevenue = [Revenue Prior Year]
RETURN
    IF(
        ISBLANK(PriorRevenue) || PriorRevenue == 0,
        BLANK(),
        DIVIDE([Total Revenue] - PriorRevenue, PriorRevenue, 0)
    )
```
*Format:* Percentage (`+0.00%;-0.00%;0.00%`)  
*Description:* Relative percentage growth compared to the identical calendar period in the previous year.

### Profit Prior Year (PY)
```dax
Profit Prior Year = 
CALCULATE(
    [Total Profit],
    SAMEPERIODLASTYEAR(Dim_Calendar[Date])
)
```

### YoY Profit Growth %
```dax
YoY Profit Growth % = 
VAR PriorProfit = [Profit Prior Year]
RETURN
    IF(
        ISBLANK(PriorProfit) || PriorProfit == 0,
        BLANK(),
        DIVIDE([Total Profit] - PriorProfit, ABS(PriorProfit), 0)
    )
```

### Revenue Year-to-Date (YTD)
```dax
Revenue YTD = 
TOTALYTD([Total Revenue], Dim_Calendar[Date])
```

---

## 4. Diagnostics & Risk Analytics

### Loss-Making Transactions Count
```dax
Loss-Making Orders Count = 
CALCULATE(
    COUNTROWS(Fact_Orders),
    Fact_Orders[profit] < 0
)
```

### Loss Rate %
```dax
Loss Rate % = 
DIVIDE([Loss-Making Orders Count], COUNTROWS(Fact_Orders), 0)
```
*Format:* Percentage (`0.00%`)  
*Description:* Proportion of order lines that generated negative net profit.

### Customer Revenue Rank
```dax
Customer Revenue Rank = 
RANKX(
    ALL(Dim_Customer[customer_name]),
    [Total Revenue],
    ,
    DESC,
    Dense
)
```
