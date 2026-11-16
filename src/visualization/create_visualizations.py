"""
Visualization generation engine for Global Retail Superstore Analytics.
Generates publication-quality charts for reports, presentations, and dashboards.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
import seaborn as sns
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Styling configuration
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams.update({
    "font.sans-serif": "Arial",
    "font.family": "sans-serif",
    "figure.titlesize": 14,
    "axes.titlesize": 12,
    "axes.labelsize": 10,
    "xtick.labelsize": 9,
    "ytick.labelsize": 9,
    "figure.autolayout": True
})

PRIMARY_COLOR = "#1f77b4"
SECONDARY_COLOR = "#ff7f0e"
ACCENT_GREEN = "#2ca02c"
ALERT_RED = "#d62728"


def save_plot(fig: plt.Figure, filepath: Path) -> None:
    filepath.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(filepath, dpi=300, bbox_inches="tight")
    plt.close(fig)
    logger.info(f"Saved figure: {filepath.name}")


def generate_all_visualizations(df: pd.DataFrame, output_dir: Path) -> list:
    saved_files = []

    # 1. Overall Sales Distribution (Log & Clean Transformed)
    fig, ax = plt.subplots(figsize=(8, 5))
    sales_clipped = df["sales"][df["sales"] <= df["sales"].quantile(0.95)]
    sns.histplot(sales_clipped, bins=40, kde=True, color=PRIMARY_COLOR, ax=ax)
    ax.set_title("1. Sales Distribution (95th Percentile Core Transactions)")
    ax.set_xlabel("Order Line Sales ($)")
    ax.set_ylabel("Transaction Frequency")
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
    p = output_dir / "01_overall_sales_distribution.png"
    save_plot(fig, p)
    saved_files.append(p)

    # 2. Monthly Sales Trend
    fig, ax = plt.subplots(figsize=(10, 5))
    monthly_sales = df.groupby("order_year_month")["sales"].sum().reset_index()
    monthly_sales["order_year_month"] = monthly_sales["order_year_month"].astype(str)
    ax.plot(monthly_sales["order_year_month"], monthly_sales["sales"], marker="o", color=PRIMARY_COLOR, linewidth=2, markersize=4)
    ax.set_title("2. Monthly Sales Trend (2011 - 2014)")
    ax.set_xlabel("Year-Month")
    ax.set_ylabel("Total Sales ($)")
    ax.set_xticks(range(0, len(monthly_sales), 4))
    ax.set_xticklabels(monthly_sales["order_year_month"].iloc[::4], rotation=45)
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
    p = output_dir / "02_monthly_sales_trend.png"
    save_plot(fig, p)
    saved_files.append(p)

    # 3. Yearly Revenue Comparison
    fig, ax = plt.subplots(figsize=(7, 5))
    yearly = df.groupby("order_year")["sales"].sum().reset_index()
    bars = ax.bar(yearly["order_year"].astype(str), yearly["sales"], color=PRIMARY_COLOR, width=0.55)
    ax.set_title("3. Yearly Revenue Comparison & Growth")
    ax.set_xlabel("Fiscal Year")
    ax.set_ylabel("Total Revenue ($)")
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
    for bar in bars:
        yval = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, yval + 50000, f"${yval/1e6:.2f}M", ha="center", va="bottom", fontsize=9, fontweight="bold")
    p = output_dir / "03_yearly_revenue_comparison.png"
    save_plot(fig, p)
    saved_files.append(p)

    # 4. Sales by Product Category
    fig, ax = plt.subplots(figsize=(7, 5))
    cat_sales = df.groupby("category")["sales"].sum().sort_values(ascending=True)
    cat_sales.plot(kind="barh", color=[PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_GREEN], ax=ax)
    ax.set_title("4. Total Sales by Product Category")
    ax.set_xlabel("Revenue ($)")
    ax.set_ylabel("Category")
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
    for i, v in enumerate(cat_sales):
        ax.text(v + 50000, i, f"${v/1e6:.2f}M", va="center", fontweight="bold", fontsize=9)
    p = output_dir / "04_sales_by_product_category.png"
    save_plot(fig, p)
    saved_files.append(p)

    # 5. Sales by Subcategory
    fig, ax = plt.subplots(figsize=(9, 7))
    subcat_sales = df.groupby("sub_category")["sales"].sum().sort_values(ascending=True)
    subcat_sales.plot(kind="barh", color=PRIMARY_COLOR, ax=ax)
    ax.set_title("5. Total Sales by Product Subcategory")
    ax.set_xlabel("Revenue ($)")
    ax.set_ylabel("Subcategory")
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
    p = output_dir / "05_sales_by_subcategory.png"
    save_plot(fig, p)
    saved_files.append(p)

    # 6. Top 10 Products by Sales
    fig, ax = plt.subplots(figsize=(9, 6))
    top_products = df.groupby("product_name")["sales"].sum().nlargest(10).sort_values(ascending=True)
    top_products.plot(kind="barh", color=ACCENT_GREEN, ax=ax)
    ax.set_title("6. Top 10 Products by Total Revenue")
    ax.set_xlabel("Total Sales ($)")
    ax.set_ylabel("Product Name")
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
    p = output_dir / "06_top_10_products_by_sales.png"
    save_plot(fig, p)
    saved_files.append(p)

    # 7. Bottom 10 Products by Sales
    fig, ax = plt.subplots(figsize=(9, 6))
    bot_products = df.groupby("product_name")["sales"].sum().nsmallest(10).sort_values(ascending=False)
    bot_products.plot(kind="barh", color=ALERT_RED, ax=ax)
    ax.set_title("7. Bottom 10 Products by Revenue (Lowest Contributors)")
    ax.set_xlabel("Total Sales ($)")
    ax.set_ylabel("Product Name")
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.2f}"))
    p = output_dir / "07_bottom_10_products_by_sales.png"
    save_plot(fig, p)
    saved_files.append(p)

    # 8. Top 10 Customers by Revenue
    fig, ax = plt.subplots(figsize=(9, 6))
    top_cust = df.groupby("customer_name")["sales"].sum().nlargest(10).sort_values(ascending=True)
    top_cust.plot(kind="barh", color=PRIMARY_COLOR, ax=ax)
    ax.set_title("8. Top 10 Customers by Total Lifetime Spend")
    ax.set_xlabel("Cumulative Spend ($)")
    ax.set_ylabel("Customer Name")
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
    p = output_dir / "08_top_10_customers_by_revenue.png"
    save_plot(fig, p)
    saved_files.append(p)

    # 9. Regional Sales Performance
    fig, ax = plt.subplots(figsize=(10, 5))
    reg_sales = df.groupby("region")["sales"].sum().sort_values(ascending=False)
    reg_sales.plot(kind="bar", color=PRIMARY_COLOR, ax=ax)
    ax.set_title("9. Regional Sales Performance")
    ax.set_xlabel("Region")
    ax.set_ylabel("Total Sales ($)")
    ax.set_xticklabels(reg_sales.index, rotation=45, ha="right")
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
    p = output_dir / "09_regional_sales_performance.png"
    save_plot(fig, p)
    saved_files.append(p)

    # 10. Profit by Region
    fig, ax = plt.subplots(figsize=(10, 5))
    reg_profit = df.groupby("region")["profit"].sum().sort_values(ascending=False)
    colors = [ACCENT_GREEN if v >= 0 else ALERT_RED for v in reg_profit]
    reg_profit.plot(kind="bar", color=colors, ax=ax)
    ax.set_title("10. Cumulative Profit by Region")
    ax.set_xlabel("Region")
    ax.set_ylabel("Total Profit ($)")
    ax.set_xticklabels(reg_profit.index, rotation=45, ha="right")
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
    p = output_dir / "10_profit_by_region.png"
    save_plot(fig, p)
    saved_files.append(p)

    # 11. Profit by Product Category
    fig, ax = plt.subplots(figsize=(7, 5))
    cat_profit = df.groupby("category")["profit"].sum().sort_values(ascending=True)
    cat_profit.plot(kind="barh", color=[SECONDARY_COLOR, PRIMARY_COLOR, ACCENT_GREEN], ax=ax)
    ax.set_title("11. Cumulative Profit by Product Category")
    ax.set_xlabel("Profit ($)")
    ax.set_ylabel("Category")
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
    p = output_dir / "11_profit_by_product_category.png"
    save_plot(fig, p)
    saved_files.append(p)

    # 12. Sales vs Profit Relationship
    fig, ax = plt.subplots(figsize=(8, 6))
    sample_df = df.sample(n=min(3000, len(df)), random_state=42)
    sns.scatterplot(data=sample_df, x="sales", y="profit", hue="category", alpha=0.6, ax=ax, palette="tab10")
    ax.set_title("12. Sales vs Profit Relationship (Sample n=3000)")
    ax.set_xlabel("Sales ($)")
    ax.set_ylabel("Profit ($)")
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
    ax.axhline(0, color="grey", linestyle="--", linewidth=1)
    p = output_dir / "12_sales_vs_profit_relationship.png"
    save_plot(fig, p)
    saved_files.append(p)

    # 13. Discount vs Profit Relationship
    fig, ax = plt.subplots(figsize=(8, 5))
    disc_summary = df.groupby(pd.cut(df["discount"], bins=[-0.01, 0, 0.1, 0.2, 0.3, 0.4, 0.5, 1.0]))["profit"].mean().reset_index()
    disc_summary["discount_bracket"] = ["0%", "0-10%", "10-20%", "20-30%", "30-40%", "40-50%", ">50%"]
    disc_summary["color"] = [ACCENT_GREEN if v >= 0 else ALERT_RED for v in disc_summary["profit"]]
    ax.bar(disc_summary["discount_bracket"], disc_summary["profit"], color=disc_summary["color"], width=0.5)
    ax.set_title("13. Impact of Discount Level on Average Transaction Profit")
    ax.set_xlabel("Discount Level Bracket")
    ax.set_ylabel("Average Profit per Line Item ($)")
    ax.axhline(0, color="black", linestyle="-", linewidth=0.8)
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
    p = output_dir / "13_discount_vs_profit_relationship.png"
    save_plot(fig, p)
    saved_files.append(p)

    # 14. Order Distribution by Segment
    fig, ax = plt.subplots(figsize=(6, 6))
    seg_counts = df.groupby("segment")["order_id"].nunique()
    ax.pie(seg_counts, labels=seg_counts.index, autopct="%1.1f%%", startangle=140, colors=[PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_GREEN], wedgeprops=dict(width=0.4, edgecolor='w'))
    ax.set_title("14. Customer Segment Order Share")
    p = output_dir / "14_order_distribution_by_segment.png"
    save_plot(fig, p)
    saved_files.append(p)

    # 15. Customer Purchase Frequency Distribution
    fig, ax = plt.subplots(figsize=(8, 5))
    cust_freq = df.groupby("customer_id")["order_id"].nunique()
    sns.histplot(cust_freq, bins=25, color=PRIMARY_COLOR, ax=ax, discrete=True)
    ax.set_title("15. Customer Purchase Frequency Distribution")
    ax.set_xlabel("Distinct Orders Placed per Customer")
    ax.set_ylabel("Number of Customers")
    p = output_dir / "15_customer_purchase_distribution.png"
    save_plot(fig, p)
    saved_files.append(p)

    # 16. Monthly Profit Trend
    fig, ax = plt.subplots(figsize=(10, 5))
    monthly_profit = df.groupby("order_year_month")["profit"].sum().reset_index()
    monthly_profit["order_year_month"] = monthly_profit["order_year_month"].astype(str)
    ax.plot(monthly_profit["order_year_month"], monthly_profit["profit"], marker="s", color=ACCENT_GREEN, linewidth=2, markersize=4)
    ax.set_title("16. Monthly Profit Trend (2011 - 2014)")
    ax.set_xlabel("Year-Month")
    ax.set_ylabel("Total Profit ($)")
    ax.set_xticks(range(0, len(monthly_profit), 4))
    ax.set_xticklabels(monthly_profit["order_year_month"].iloc[::4], rotation=45)
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
    p = output_dir / "16_monthly_profit_trend.png"
    save_plot(fig, p)
    saved_files.append(p)

    # 17. Sales Growth Analysis
    fig, ax = plt.subplots(figsize=(8, 5))
    yearly_growth = df.groupby("order_year")["sales"].sum().pct_change().dropna() * 100
    bars = ax.bar(yearly_growth.index.astype(str), yearly_growth.values, color=PRIMARY_COLOR, width=0.45)
    ax.set_title("17. Year-over-Year Revenue Growth Rate (%)")
    ax.set_xlabel("Year")
    ax.set_ylabel("YoY Growth (%)")
    for bar in bars:
        h = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, h + 0.5, f"{h:.1f}%", ha="center", fontweight="bold")
    p = output_dir / "17_sales_growth_analysis.png"
    save_plot(fig, p)
    saved_files.append(p)

    # 18. Shipping Mode Analysis
    fig, ax = plt.subplots(figsize=(8, 5))
    ship_summary = df.groupby("ship_mode").agg(total_orders=("order_id", "nunique"), avg_days=("shipping_duration_days", "mean")).reset_index()
    sns.barplot(data=ship_summary, x="ship_mode", y="total_orders", palette="Blues_r", ax=ax)
    ax.set_title("18. Order Volume by Shipping Mode")
    ax.set_xlabel("Shipping Mode")
    ax.set_ylabel("Distinct Orders")
    p = output_dir / "18_shipping_mode_analysis.png"
    save_plot(fig, p)
    saved_files.append(p)

    # 19. Geographic Sales Comparison (Top 15 Countries)
    fig, ax = plt.subplots(figsize=(9, 6))
    top_countries = df.groupby("country")["sales"].sum().nlargest(15).sort_values(ascending=True)
    top_countries.plot(kind="barh", color=PRIMARY_COLOR, ax=ax)
    ax.set_title("19. Top 15 Revenue Contributing Countries")
    ax.set_xlabel("Total Sales ($)")
    ax.set_ylabel("Country")
    ax.xaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
    p = output_dir / "19_top_15_countries_sales.png"
    save_plot(fig, p)
    saved_files.append(p)

    # 20. Category and Market Performance Heatmap
    fig, ax = plt.subplots(figsize=(8, 5))
    pivot_profit = df.pivot_table(index="category", columns="market", values="profit", aggfunc="sum")
    sns.heatmap(pivot_profit / 1000, annot=True, fmt=".1f", cmap="YlGnBu", ax=ax, cbar_kws={'label': 'Profit ($K)'})
    ax.set_title("20. Profitability Matrix: Category vs Market ($ in Thousands)")
    ax.set_xlabel("Market")
    ax.set_ylabel("Category")
    p = output_dir / "20_category_market_profit_heatmap.png"
    save_plot(fig, p)
    saved_files.append(p)

    logger.info(f"Generated {len(saved_files)} visualizations successfully.")
    return saved_files


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parents[2]
    data_path = base_dir / "data" / "processed" / "cleaned_global_superstore.csv"
    fig_dir = base_dir / "reports" / "figures"
    df = pd.read_csv(data_path)
    generate_all_visualizations(df, fig_dir)
