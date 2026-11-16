"""
Unit tests for executive KPI calculations and mathematical formulas.
"""

import pytest
import pandas as pd
from pathlib import Path
from src.analysis.kpi_calculations import calculate_overall_kpis, calculate_yearly_kpis


@pytest.fixture(scope="module")
def processed_df():
    path = Path("data/processed/cleaned_global_superstore.csv")
    return pd.read_csv(path)


def test_overall_kpis(processed_df):
    kpis = calculate_overall_kpis(processed_df)
    assert kpis["total_revenue"] == 12642501.91
    assert kpis["total_profit"] == 1467457.29
    assert kpis["total_orders"] == 25035
    assert kpis["customer_count"] == 1590
    assert kpis["average_order_value"] == 504.99
    assert kpis["profit_margin_pct"] == 11.61
    assert kpis["revenue_cagr_pct"] == 23.92


def test_yearly_kpis_growth(processed_df):
    yearly = calculate_yearly_kpis(processed_df)
    assert len(yearly) == 4
    # Check 2012 YoY growth is approx 18.50%
    row_2012 = yearly[yearly["order_year"] == 2012].iloc[0]
    assert abs(row_2012["revenue_growth_pct"] - 18.50) < 0.1
    # Check 2013 YoY growth is approx 27.20%
    row_2013 = yearly[yearly["order_year"] == 2013].iloc[0]
    assert abs(row_2013["revenue_growth_pct"] - 27.20) < 0.1


def test_no_zero_division():
    empty_df = pd.DataFrame(columns=["sales", "profit", "order_id", "customer_id", "quantity", "order_year"])
    kpis = calculate_overall_kpis(empty_df)
    assert kpis["total_revenue"] == 0.0
    assert kpis["average_order_value"] == 0.0
    assert kpis["profit_margin_pct"] == 0.0
