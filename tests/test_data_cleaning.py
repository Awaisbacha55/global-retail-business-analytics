"""
Unit tests for data loading, cleaning, and text standardization.
"""

import pytest
import pandas as pd
from pathlib import Path
from src.data.load_data import load_raw_dataset, inspect_raw_data
from src.data.clean_data import clean_dataset, standardize_column_names, handle_missing_values


@pytest.fixture(scope="module")
def raw_df():
    return load_raw_dataset()


def test_raw_dataset_loading(raw_df):
    assert raw_df is not None
    assert len(raw_df) == 51290
    assert len(raw_df.columns) == 24


def test_standardize_column_names():
    test_df = pd.DataFrame({"Order ID": ["CA-1"], "Ship-Date": ["2012-01-01"], " Sales ": [100.0]})
    cleaned = standardize_column_names(test_df)
    assert "order_id" in cleaned.columns
    assert "ship_date" in cleaned.columns
    assert "sales" in cleaned.columns


def test_missing_values_treatment(raw_df):
    cleaned_df, audit = clean_dataset(raw_df)
    assert cleaned_df["postal_code"].isnull().sum() == 0
    assert "Unknown" in cleaned_df["postal_code"].values
    assert len(cleaned_df) == 51290


def test_no_critical_nulls(raw_df):
    cleaned_df, _ = clean_dataset(raw_df)
    for col in ["order_id", "customer_id", "product_id", "sales", "profit", "quantity"]:
        assert cleaned_df[col].isnull().sum() == 0
