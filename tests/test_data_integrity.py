"""
Integration tests for dataset integrity, feature engineering, and file generation.
"""

import pytest
import pandas as pd
from pathlib import Path


@pytest.fixture(scope="module")
def processed_df():
    path = Path("data/processed/cleaned_global_superstore.csv")
    return pd.read_csv(path)


def test_chronological_sequence(processed_df):
    processed_df["order_date"] = pd.to_datetime(processed_df["order_date"])
    processed_df["ship_date"] = pd.to_datetime(processed_df["ship_date"])
    invalid_rows = processed_df[processed_df["ship_date"] < processed_df["order_date"]]
    assert len(invalid_rows) == 0


def test_positive_financial_values(processed_df):
    assert (processed_df["sales"] > 0).all()
    assert (processed_df["quantity"] > 0).all()
    assert (processed_df["shipping_cost"] >= 0).all()
    assert (processed_df["discount"] >= 0).all()
    assert (processed_df["discount"] <= 1.0).all()


def test_engineered_features_presence(processed_df):
    required_features = [
        "order_year", "order_month", "order_quarter", "shipping_duration_days",
        "profit_margin_pct", "unit_price", "unit_cost", "is_profitable", "is_loss"
    ]
    for feat in required_features:
        assert feat in processed_df.columns


def test_generated_artifacts_existence():
    assert Path("data/processed/cleaned_global_superstore.csv").exists()
    assert Path("dashboard/exports/powerbi_superstore_model.csv").exists()
    assert Path("dashboard/exports/Dim_Calendar.csv").exists()
    assert Path("dashboard/exports/Dim_Customer.csv").exists()
    assert Path("dashboard/exports/Dim_Product.csv").exists()
    assert Path("dashboard/exports/Fact_Orders.csv").exists()
    assert Path("reports/final_project_report.pdf").exists()
    assert Path("models/sales_forecasting/forecast_validation_plot.png").exists()
    assert Path("models/customer_segmentation/customer_segments_scatter.png").exists()
