"""
Core KPI calculation module for Global Retail Superstore Analytics.
Calculates high-level executive metrics, period-over-period growth rates,
and dimensional profitability figures.
"""

from typing import Dict, Any, Optional
import pandas as pd
import numpy as np


def calculate_overall_kpis(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Calculate the primary executive business KPIs across the full dataset:
    1. Total Revenue
    2. Total Profit
    3. Total Orders (Distinct Order IDs)
    4. Average Order Value (AOV)
    5. Profit Margin (%)
    6. Customer Count (Distinct Customer IDs)
    7. Overall Annualized Growth Rate (CAGR)
    """
    total_revenue = float(df["sales"].sum())
    total_profit = float(df["profit"].sum())
    total_orders = int(df["order_id"].nunique())
    customer_count = int(df["customer_id"].nunique())
    
    aov = (total_revenue / total_orders) if total_orders > 0 else 0.0
    profit_margin = ((total_profit / total_revenue) * 100.0) if total_revenue > 0 else 0.0
    
    # Calculate Year-over-Year Growth
    if "order_year" in df.columns:
        yearly_rev = df.groupby("order_year")["sales"].sum().sort_index()
        years = yearly_rev.index.tolist()
        if len(years) > 1:
            first_year_rev = float(yearly_rev.iloc[0])
            last_year_rev = float(yearly_rev.iloc[-1])
            num_periods = len(years) - 1
            cagr = (((last_year_rev / first_year_rev) ** (1.0 / num_periods)) - 1.0) * 100.0
        else:
            cagr = 0.0
    else:
        cagr = 0.0

    return {
        "total_revenue": round(total_revenue, 2),
        "total_profit": round(total_profit, 2),
        "total_orders": total_orders,
        "average_order_value": round(aov, 2),
        "profit_margin_pct": round(profit_margin, 2),
        "customer_count": customer_count,
        "revenue_cagr_pct": round(cagr, 2),
        "total_quantity": int(df["quantity"].sum())
    }


def calculate_yearly_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate KPIs broken down by fiscal year, including YoY revenue growth.
    """
    yearly = df.groupby("order_year").agg(
        total_revenue=("sales", "sum"),
        total_profit=("profit", "sum"),
        total_orders=("order_id", "nunique"),
        customer_count=("customer_id", "nunique"),
        total_quantity=("quantity", "sum")
    ).reset_index()

    yearly["average_order_value"] = (yearly["total_revenue"] / yearly["total_orders"]).round(2)
    yearly["profit_margin_pct"] = ((yearly["total_profit"] / yearly["total_revenue"]) * 100.0).round(2)
    yearly["revenue_growth_pct"] = (yearly["total_revenue"].pct_change() * 100.0).round(2).fillna(0.0)
    yearly["profit_growth_pct"] = (yearly["total_profit"].pct_change() * 100.0).round(2).fillna(0.0)
    yearly["order_growth_pct"] = (yearly["total_orders"].pct_change() * 100.0).round(2).fillna(0.0)

    yearly["total_revenue"] = yearly["total_revenue"].round(2)
    yearly["total_profit"] = yearly["total_profit"].round(2)
    return yearly


def calculate_category_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize performance metrics by product category.
    """
    cat_summary = df.groupby("category").agg(
        revenue=("sales", "sum"),
        profit=("profit", "sum"),
        orders=("order_id", "nunique"),
        quantity=("quantity", "sum"),
        avg_discount=("discount", "mean")
    ).reset_index()

    cat_summary["profit_margin_pct"] = ((cat_summary["profit"] / cat_summary["revenue"]) * 100.0).round(2)
    cat_summary["revenue_share_pct"] = ((cat_summary["revenue"] / df["sales"].sum()) * 100.0).round(2)
    cat_summary["avg_discount_pct"] = (cat_summary["avg_discount"] * 100.0).round(2)
    cat_summary["revenue"] = cat_summary["revenue"].round(2)
    cat_summary["profit"] = cat_summary["profit"].round(2)
    return cat_summary.sort_values(by="revenue", ascending=False)


def calculate_regional_kpis(df: pd.DataFrame) -> pd.DataFrame:
    """
    Summarize revenue and profitability by geographic market and region.
    """
    reg_summary = df.groupby(["market", "region"]).agg(
        revenue=("sales", "sum"),
        profit=("profit", "sum"),
        orders=("order_id", "nunique"),
        customers=("customer_id", "nunique")
    ).reset_index()

    reg_summary["profit_margin_pct"] = ((reg_summary["profit"] / reg_summary["revenue"]) * 100.0).round(2)
    reg_summary["aov"] = (reg_summary["revenue"] / reg_summary["orders"]).round(2)
    reg_summary["revenue"] = reg_summary["revenue"].round(2)
    reg_summary["profit"] = reg_summary["profit"].round(2)
    return reg_summary.sort_values(by="revenue", ascending=False)
