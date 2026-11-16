"""
End-to-end data preparation script.
Loads raw dataset, cleans records, enriches with features,
and exports processed files for analytics, machine learning, and Power BI.
"""

from pathlib import Path
import logging
from src.data.load_data import load_raw_dataset, inspect_raw_data
from src.data.clean_data import clean_dataset
from src.data.feature_engineering import engineer_features

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def run_data_preparation() -> Path:
    logger.info("Executing Step 1: Loading raw data...")
    df_raw = load_raw_dataset()
    raw_info = inspect_raw_data(df_raw)
    logger.info(f"Loaded {raw_info['total_records']:,} rows, {raw_info['total_columns']} columns.")

    logger.info("Executing Step 2: Cleaning dataset...")
    df_clean, clean_audit = clean_dataset(df_raw)
    logger.info(f"Cleaned dataset: {df_clean.shape[0]:,} rows, {df_clean.shape[1]} columns.")

    logger.info("Executing Step 3: Feature engineering...")
    df_feat, feat_meta = engineer_features(df_clean)
    logger.info(f"Final feature dataset: {df_feat.shape[0]:,} rows, {df_feat.shape[1]} columns.")

    # Export locations
    base_dir = Path(__file__).resolve().parents[2]
    processed_dir = base_dir / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    out_csv = processed_dir / "cleaned_global_superstore.csv"

    pbi_dir = base_dir / "dashboard" / "exports"
    pbi_dir.mkdir(parents=True, exist_ok=True)
    pbi_csv = pbi_dir / "powerbi_superstore_model.csv"

    logger.info(f"Exporting processed CSV to: {out_csv}")
    df_feat.to_csv(out_csv, index=False)

    logger.info(f"Exporting Power BI CSV to: {pbi_csv}")
    df_feat.to_csv(pbi_csv, index=False)

    logger.info("Data preparation pipeline successfully completed.")
    return out_csv


if __name__ == "__main__":
    run_data_preparation()
