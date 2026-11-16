"""
Data loading module for Global Superstore raw dataset.
Handles file ingestion, encoding detection, and initial integrity checks.
"""

from pathlib import Path
from typing import Optional, Tuple
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def load_raw_dataset(
    file_path: Optional[Path] = None,
    encoding: str = "latin-1",
    fallback_excel: bool = True
) -> pd.DataFrame:
    """
    Load raw transaction records from CSV with fallback to Excel.
    
    Parameters
    ----------
    file_path : Optional[Path]
        Direct path to dataset file. Defaults to data/raw/Global_Superstore2.csv.
    encoding : str
        Character encoding for CSV parsing. Default is 'latin-1'.
    fallback_excel : bool
        Whether to attempt loading XLSX if CSV fails or is missing.
        
    Returns
    -------
    pd.DataFrame
        Loaded pandas DataFrame.
    """
    if file_path is None:
        base_dir = Path(__file__).resolve().parents[2]
        file_path = base_dir / "data" / "raw" / "Global_Superstore2.csv"
        alt_path = base_dir / "data" / "raw" / "Global_Superstore2.xlsx"
    else:
        file_path = Path(file_path)
        alt_path = file_path.with_suffix(".xlsx")

    if file_path.exists():
        logger.info(f"Loading CSV data from: {file_path}")
        try:
            df = pd.read_csv(file_path, encoding=encoding, low_memory=False)
            logger.info(f"Loaded {len(df):,} records across {len(df.columns)} columns.")
            return df
        except UnicodeDecodeError:
            logger.warning(f"Encoding {encoding} failed. Retrying with utf-8-sig...")
            df = pd.read_csv(file_path, encoding="utf-8-sig", low_memory=False)
            return df

    if fallback_excel and alt_path.exists():
        logger.info(f"CSV not found. Loading Excel workbook from: {alt_path}")
        df = pd.read_excel(alt_path)
        logger.info(f"Loaded {len(df):,} records from Excel.")
        return df

    raise FileNotFoundError(f"Neither CSV nor Excel found at {file_path} or {alt_path}")


def inspect_raw_data(df: pd.DataFrame) -> dict:
    """
    Extract structural metrics and missing value summary for profiling.
    """
    total_records = len(df)
    total_columns = len(df.columns)
    duplicate_rows = int(df.duplicated().sum())
    missing_by_col = df.isnull().sum()
    missing_cols = missing_by_col[missing_by_col > 0].to_dict()

    summary = {
        "total_records": total_records,
        "total_columns": total_columns,
        "duplicate_rows": duplicate_rows,
        "missing_columns": missing_cols,
        "memory_mb": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
        "column_names": list(df.columns),
        "dtypes": {col: str(dtype) for col, dtype in df.dtypes.items()}
    }
    return summary


if __name__ == "__main__":
    df_raw = load_raw_dataset()
    info = inspect_raw_data(df_raw)
    print("Dataset Inspection Summary:")
    for k, v in info.items():
        if k != "column_names" and k != "dtypes":
            print(f"  {k}: {v}")
