"""
Feature engineering module for Global Retail Superstore dataset.
Enriches transactional records with temporal attributes, profitability indicators,
shipping metrics, customer aggregation statistics, and product pricing dimensions.
"""

from typing import Tuple, Dict, Any
import numpy as np
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def add_date_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Extract calendar dimensions and operational fulfillment durations.
    """
    df = df.copy()
    if "order_date" in df.columns:
        df["order_year"] = df["order_date"].dt.year
        df["order_month"] = df["order_date"].dt.month
        df["order_month_name"] = df["order_date"].dt.strftime("%b")
        df["order_quarter"] = "Q" + df["order_date"].dt.quarter.astype(str)
        df["order_year_quarter"] = df["order_year"].astype(str) + "-" + df["order_quarter"]
        df["order_day"] = df["order_date"].dt.day
        df["order_day_name"] = df["order_date"].dt.day_name()
        df["order_year_month"] = df["order_date"].dt.to_period("M").astype(str)

    if "order_date" in df.columns and "ship_date" in df.columns:
        df["shipping_duration_days"] = (df["ship_date"] - df["order_date"]).dt.days
        # Clean any negative anomalies if any
        df["shipping_duration_days"] = df["shipping_duration_days"].clip(lower=0)
        
    return df


def add_financial_and_margin_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute operational margins, unit costs, and profit thresholds.
    """
    df = df.copy()
    
    # Avoid zero-division in profit margin
    df["profit_margin_pct"] = np.where(
        df["sales"] > 0,
        (df["profit"] / df["sales"]) * 100.0,
        0.0
    ).round(2)
    
    # Unit prices and approximate unit cost
    df["unit_price"] = np.where(
        df["quantity"] > 0,
        df["sales"] / df["quantity"],
        0.0
    ).round(2)
    
    df["unit_cost"] = np.where(
        df["quantity"] > 0,
        (df["sales"] - df["profit"]) / df["quantity"],
        0.0
    ).round(2)
    
    # Financial flags
    df["is_profitable"] = (df["profit"] > 0).astype(int)
    df["is_loss"] = (df["profit"] < 0).astype(int)
    df["has_discount"] = (df["discount"] > 0).astype(int)
    
    # Shipping cost ratio
    df["shipping_cost_ratio_pct"] = np.where(
        df["sales"] > 0,
        (df["shipping_cost"] / df["sales"]) * 100.0,
        0.0
    ).round(2)
    
    return df


def add_customer_and_order_aggregations(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate customer transaction frequencies and cumulative monetary contributions.
    """
    df = df.copy()
    
    # Order-level total revenue
    order_totals = df.groupby("order_id")["sales"].transform("sum").round(2)
    df["order_total_sales"] = order_totals
    
    # Order-level distinct item count
    order_items = df.groupby("order_id")["product_id"].transform("count")
    df["order_item_count"] = order_items
    
    # Customer-level metrics
    cust_orders = df.groupby("customer_id")["order_id"].transform("nunique")
    cust_sales = df.groupby("customer_id")["sales"].transform("sum").round(2)
    cust_profit = df.groupby("customer_id")["profit"].transform("sum").round(2)
    
    df["customer_order_frequency"] = cust_orders
    df["customer_lifetime_sales"] = cust_sales
    df["customer_lifetime_profit"] = cust_profit
    
    return df


def engineer_features(df_cleaned: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Execute full feature engineering pipeline.
    """
    logger.info("Executing feature engineering pipeline...")
    initial_cols = len(df_cleaned.columns)
    
    df_temporal = add_date_features(df_cleaned)
    df_financial = add_financial_and_margin_features(df_temporal)
    df_featured = add_customer_and_order_aggregations(df_financial)
    
    new_cols = [c for c in df_featured.columns if c not in df_cleaned.columns]
    logger.info(f"Engineered {len(new_cols)} additional features: {new_cols}")
    
    metadata = {
        "initial_features": initial_cols,
        "final_features": len(df_featured.columns),
        "engineered_feature_names": new_cols
    }
    return df_featured, metadata
