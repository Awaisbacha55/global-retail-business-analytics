"""
Data cleaning and preprocessing module for Global Superstore dataset.
Provides missing value treatment, type conversions, text standardization,
and data integrity verification.
"""

from pathlib import Path
from typing import Tuple, Dict, Any
import numpy as np
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize DataFrame column names to consistent lower snake_case.
    """
    cleaned_cols = (
        df.columns.str.strip()
        .str.lower()
        .str.replace(" ", "_", regex=False)
        .str.replace("-", "_", regex=False)
    )
    df = df.copy()
    df.columns = cleaned_cols
    return df


def parse_datetime_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Parse order_date and ship_date to pandas datetime using dayfirst=True.
    Validates logical temporal sequence (ship_date >= order_date).
    """
    df = df.copy()
    for col in ["order_date", "ship_date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], dayfirst=True, errors="coerce")
            
    # Check date integrity
    if "order_date" in df.columns and "ship_date" in df.columns:
        invalid_dates = df[df["ship_date"] < df["order_date"]]
        if len(invalid_dates) > 0:
            logger.warning(f"Found {len(invalid_dates)} records where ship_date < order_date.")
    return df


def handle_missing_values(df: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Handle missing values with explicit business justifications.
    In Global Superstore, postal_code is predominantly populated for US markets.
    Missing postal codes for international transactions are categorized as 'Unknown'.
    """
    df = df.copy()
    missing_before = df.isnull().sum().to_dict()
    
    if "postal_code" in df.columns:
        # Standardize US postal codes to 5-digit strings, rest as 'Unknown'
        df["postal_code"] = df["postal_code"].apply(
            lambda x: f"{int(x):05d}" if pd.notnull(x) and str(x).replace(".", "").isdigit() else "Unknown"
        )
    
    # Check for any remaining nulls in critical business fields
    critical_cols = ["order_id", "customer_id", "product_id", "sales", "profit", "quantity"]
    for col in critical_cols:
        if col in df.columns and df[col].isnull().sum() > 0:
            logger.warning(f"Imputing or filtering {df[col].isnull().sum()} nulls in {col}")
            df = df.dropna(subset=[col])
            
    missing_after = df.isnull().sum().to_dict()
    summary = {
        "missing_before": {k: int(v) for k, v in missing_before.items() if v > 0},
        "missing_after": {k: int(v) for k, v in missing_after.items() if v > 0}
    }
    return df, summary


def clean_text_and_categories(df: pd.DataFrame) -> pd.DataFrame:
    """
    Trim whitespace and harmonize categorical values across the dataset.
    """
    df = df.copy()
    text_cols = [
        "customer_name", "segment", "city", "state", "country",
        "market", "region", "category", "sub_category", "product_name",
        "order_priority", "ship_mode"
    ]
    for col in text_cols:
        if col in df.columns and df[col].dtype == "object":
            df[col] = df[col].astype(str).str.strip()
            
    return df


def enforce_numeric_types(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ensure financial and quantitative fields have strict numeric dtypes.
    """
    df = df.copy()
    numeric_spec = {
        "sales": float,
        "quantity": int,
        "discount": float,
        "profit": float,
        "shipping_cost": float,
        "row_id": int
    }
    for col, target_type in numeric_spec.items():
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype(target_type)
            
    return df


def clean_dataset(df_raw: pd.DataFrame) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Execute end-to-end data cleaning workflow.
    """
    logger.info("Starting dataset cleaning pipeline...")
    initial_shape = df_raw.shape
    
    df_std = standardize_column_names(df_raw)
    
    # Duplicate check
    duplicates_count = int(df_std.duplicated().sum())
    if duplicates_count > 0:
        logger.info(f"Removing {duplicates_count} exact duplicate rows.")
        df_std = df_std.drop_duplicates()
        
    df_dates = parse_datetime_columns(df_std)
    df_imputed, missing_audit = handle_missing_values(df_dates)
    df_text = clean_text_and_categories(df_imputed)
    df_clean = enforce_numeric_types(df_text)
    
    final_shape = df_clean.shape
    logger.info(f"Cleaning complete. Shape transitioned from {initial_shape} to {final_shape}.")
    
    audit_report = {
        "initial_rows": initial_shape[0],
        "final_rows": final_shape[0],
        "initial_cols": initial_shape[1],
        "final_cols": final_shape[1],
        "duplicates_removed": duplicates_count,
        "missing_audit": missing_audit
    }
    return df_clean, audit_report
