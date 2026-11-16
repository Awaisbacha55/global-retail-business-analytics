"""
Configuration settings for Global Retail Business Analytics & Decision Intelligence.
Defines base paths, dataset parameters, color palettes, and global constants.
"""

from pathlib import Path

# Base Paths
PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"

REPORTS_DIR = PROJECT_ROOT / "reports"
FIGURES_DIR = REPORTS_DIR / "figures"
MODELS_DIR = PROJECT_ROOT / "models"
SALES_MODELS_DIR = MODELS_DIR / "sales_forecasting"
CUSTOMER_MODELS_DIR = MODELS_DIR / "customer_segmentation"

SQL_DIR = PROJECT_ROOT / "sql"
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"
DASHBOARD_DIR = PROJECT_ROOT / "dashboard"
POWERBI_DIR = DASHBOARD_DIR / "powerbi"
EXPORTS_DIR = DASHBOARD_DIR / "exports"
DOCS_DIR = PROJECT_ROOT / "docs"

# Dataset Files
RAW_CSV_PATH = RAW_DATA_DIR / "Global_Superstore2.csv"
RAW_XLSX_PATH = RAW_DATA_DIR / "Global_Superstore2.xlsx"
CLEANED_CSV_PATH = PROCESSED_DATA_DIR / "cleaned_global_superstore.csv"
POWERBI_CSV_PATH = EXPORTS_DIR / "powerbi_superstore_model.csv"

# Color Palettes for Consistent Visualizations
PRIMARY_COLOR = "#1f77b4"
SECONDARY_COLOR = "#ff7f0e"
ACCENT_COLOR = "#2ca02c"
DANGER_COLOR = "#d62728"
PALETTE_CATEGORICAL = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b"]
PALETTE_DIVERGING = "vlag"
PALETTE_SEQUENTIAL = "Blues"

# Project Metadata
PROJECT_NAME = "Global Retail Business Analytics & Decision Intelligence"
AUTHOR_NAME = "Muhammad Awais Bacha"
ORGANIZATION = "Devixo Solutions"
TASK_NAME = "Task 04 - Complete Business Analytics Project"
RANDOM_STATE = 42
