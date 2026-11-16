"""
Sales forecasting module for Global Retail Superstore.
Aggregates sales by monthly frequency, builds feature-engineered lag/rolling predictors,
evaluates against baseline models, and produces defensible out-of-sample forecasts.
"""

from pathlib import Path
from typing import Dict, Any, Tuple
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, mean_absolute_percentage_error
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def prepare_monthly_series(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate transaction sales into a contiguous monthly time series.
    """
    df = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df["order_date"]):
        df["order_date"] = pd.to_datetime(df["order_date"], dayfirst=True)
        
    monthly = df.set_index("order_date").resample("ME")["sales"].sum().reset_index()
    monthly.rename(columns={"order_date": "ds", "sales": "y"}, inplace=True)
    monthly["month_idx"] = np.arange(len(monthly))
    monthly["month_of_year"] = monthly["ds"].dt.month
    monthly["quarter"] = monthly["ds"].dt.quarter
    
    # Lag and rolling features
    monthly["lag_1"] = monthly["y"].shift(1)
    monthly["lag_2"] = monthly["y"].shift(2)
    monthly["lag_3"] = monthly["y"].shift(3)
    monthly["lag_12"] = monthly["y"].shift(12)
    monthly["rolling_mean_3"] = monthly["y"].shift(1).rolling(window=3).mean()
    monthly["rolling_mean_6"] = monthly["y"].shift(1).rolling(window=6).mean()
    
    return monthly


def evaluate_forecast(y_true: np.ndarray, y_pred: np.ndarray) -> Dict[str, float]:
    """
    Calculate MAE, RMSE, and MAPE.
    """
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = mean_absolute_percentage_error(y_true, y_pred) * 100.0
    return {
        "MAE": round(float(mae), 2),
        "RMSE": round(float(rmse), 2),
        "MAPE": round(float(mape), 2)
    }


def train_and_evaluate_forecasting(
    monthly_df: pd.DataFrame,
    test_months: int = 12,
    output_dir: Optional[Path] = None
) -> Tuple[Dict[str, Any], pd.DataFrame]:
    """
    Chronological train/test split:
    Train on historical period (e.g. 2011-2013 = 36 months),
    Test on hold-out period (2014 = 12 months).
    """
    # Filter valid rows with lag features
    feature_cols = ["month_idx", "month_of_year", "quarter", "lag_1", "lag_2", "lag_3", "lag_12", "rolling_mean_3", "rolling_mean_6"]
    valid_df = monthly_df.dropna(subset=feature_cols).copy()
    
    train = valid_df.iloc[:-test_months].copy()
    test = valid_df.iloc[-test_months:].copy()
    
    X_train, y_train = train[feature_cols], train["y"]
    X_test, y_test = test[feature_cols], test["y"]
    
    # Baseline 1: Naive (previous month)
    y_pred_naive = test["lag_1"].values
    baseline_naive_metrics = evaluate_forecast(y_test.values, y_pred_naive)
    
    # Baseline 2: Moving Average (rolling 3 months)
    y_pred_ma3 = test["rolling_mean_3"].values
    baseline_ma_metrics = evaluate_forecast(y_test.values, y_pred_ma3)
    
    # Machine Learning Model: Random Forest Regressor
    rf = RandomForestRegressor(n_estimators=100, max_depth=5, random_state=42)
    rf.fit(X_train, y_train)
    y_pred_rf = rf.predict(X_test)
    rf_metrics = evaluate_forecast(y_test.values, y_pred_rf)
    
    logger.info(f"Forecasting Evaluation (Test n={test_months}):")
    logger.info(f"  Naive Baseline:       {baseline_naive_metrics}")
    logger.info(f"  3-Month MA Baseline:  {baseline_ma_metrics}")
    logger.info(f"  Random Forest Model:  {rf_metrics}")
    
    # Forecast plot
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(train["ds"], train["y"], label="Historical Training (2012-2013)", color="#1f77b4", linewidth=2)
        ax.plot(test["ds"], test["y"], label="Actual Sales (2014 Holdout)", color="#2ca02c", linewidth=2, marker="o")
        ax.plot(test["ds"], y_pred_rf, label=f"Random Forest Forecast (MAPE: {rf_metrics['MAPE']}%)", color="#ff7f0e", linewidth=2, linestyle="--", marker="s")
        ax.plot(test["ds"], y_pred_naive, label="Naive Baseline", color="#7f7f7f", linewidth=1, linestyle=":")
        
        ax.set_title("Time-Series Sales Forecasting: Actual vs Predicted (2014 Validation)")
        ax.set_xlabel("Date")
        ax.set_ylabel("Monthly Revenue ($)")
        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
        ax.legend(loc="upper left")
        
        plot_path = output_dir / "forecast_validation_plot.png"
        fig.savefig(plot_path, dpi=300, bbox_inches="tight")
        plt.close(fig)
        logger.info(f"Saved forecast evaluation plot to {plot_path}")
        
    results = {
        "baseline_naive": baseline_naive_metrics,
        "baseline_ma": baseline_ma_metrics,
        "random_forest": rf_metrics,
        "train_period": f"{train['ds'].min().strftime('%Y-%m')} to {train['ds'].max().strftime('%Y-%m')}",
        "test_period": f"{test['ds'].min().strftime('%Y-%m')} to {test['ds'].max().strftime('%Y-%m')}"
    }
    
    test_results_df = test[["ds", "y"]].copy()
    test_results_df["predicted_rf"] = y_pred_rf
    test_results_df["predicted_naive"] = y_pred_naive
    test_results_df["predicted_ma3"] = y_pred_ma3
    
    return results, test_results_df


if __name__ == "__main__":
    from src.data.load_data import load_raw_dataset
    from src.data.clean_data import clean_dataset
    
    base_dir = Path(__file__).resolve().parents[2]
    df_raw = load_raw_dataset()
    df_clean, _ = clean_dataset(df_raw)
    monthly = prepare_monthly_series(df_clean)
    
    out_dir = base_dir / "models" / "sales_forecasting"
    metrics, pred_df = train_and_evaluate_forecasting(monthly, test_months=12, output_dir=out_dir)
    print("Forecasting results:")
    for k, v in metrics.items():
        print(f"  {k}: {v}")
