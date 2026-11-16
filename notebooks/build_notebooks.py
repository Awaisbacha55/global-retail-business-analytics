"""
Automated notebook builder for Global Retail Superstore Analytics.
Generates all 6 comprehensive Jupyter notebooks with detailed markdown analysis and executable code.
"""

from pathlib import Path
import nbformat as nbf


def make_nb():
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.12"
        }
    }
    return nb


def create_all_notebooks(notebooks_dir: Path):
    notebooks_dir.mkdir(parents=True, exist_ok=True)

    # 1. 01_dataset_inspection.ipynb
    nb1 = make_nb()
    nb1.cells = [
        nbf.v4.new_markdown_cell(
            "# 01. Dataset Inspection & Initial Profiling\n"
            "**Project:** Global Retail Business Analytics & Decision Intelligence  \n"
            "**Author:** Muhammad Awais Bacha | Devixo Solutions  \n\n"
            "### Objectives:\n"
            "- Ingest raw Global Superstore dataset (CSV / Excel)\n"
            "- Profile total records, columns, types, and memory footprint\n"
            "- Identify missing values, duplicate records, and initial distribution anomalies."
        ),
        nbf.v4.new_code_cell(
            "import pandas as pd\n"
            "import numpy as np\n"
            "from pathlib import Path\n"
            "from src.data.load_data import load_raw_dataset, inspect_raw_data\n\n"
            "df_raw = load_raw_dataset()\n"
            "info = inspect_raw_data(df_raw)\n\n"
            "print(f'Total Rows: {info[\"total_records\"]:,}')\n"
            "print(f'Total Columns: {info[\"total_columns\"]}')\n"
            "print(f'Duplicate Rows: {info[\"duplicate_rows\"]}')\n"
            "print(f'Memory Footprint: {info[\"memory_mb\"]} MB')\n"
            "print('\\nMissing Values Count:')\n"
            "for col, count in info['missing_columns'].items():\n"
            "    print(f'  {col}: {count:,} ({count / info[\"total_records\"] * 100:.2f}%)')\n"
            "df_raw.head(3)"
        ),
        nbf.v4.new_markdown_cell(
            "### Structural Analysis Summary\n"
            "- The dataset comprises exactly **51,290 transactions** across **24 features**.\n"
            "- Zero exact duplicate rows exist.\n"
            "- The only attribute exhibiting missing values is `Postal Code` (41,296 nulls, 80.5%).\n"
            "- Investigation demonstrates this is because only US domestic orders have postal codes; non-US records do not carry US ZIP codes."
        )
    ]
    with open(notebooks_dir / "01_dataset_inspection.ipynb", "w", encoding="utf-8") as f:
        nbf.write(nb1, f)

    # 2. 02_data_cleaning.ipynb
    nb2 = make_nb()
    nb2.cells = [
        nbf.v4.new_markdown_cell(
            "# 02. Data Cleaning & Preprocessing Pipeline\n"
            "**Project:** Global Retail Business Analytics & Decision Intelligence  \n"
            "**Author:** Muhammad Awais Bacha | Devixo Solutions  \n\n"
            "### Objectives:\n"
            "- Standardize column nomenclature to snake_case\n"
            "- Parse date features with chronological integrity\n"
            "- Handle missing values in Postal Code with business justification\n"
            "- Validate numeric ranges and strip extraneous whitespace."
        ),
        nbf.v4.new_code_cell(
            "from src.data.load_data import load_raw_dataset\n"
            "from src.data.clean_data import clean_dataset\n\n"
            "df_raw = load_raw_dataset()\n"
            "df_clean, audit = clean_dataset(df_raw)\n"
            "print('Data Cleaning Audit Report:')\n"
            "for k, v in audit.items():\n"
            "    print(f'  {k}: {v}')\n"
            "df_clean.info()"
        ),
        nbf.v4.new_markdown_cell(
            "### Data Cleaning Methodology\n"
            "- Preserved 100% of the 51,290 transactions.\n"
            "- Standardized US postal codes to 5-digit strings, tagged non-US orders as `'Unknown'`.\n"
            "- Converted `order_date` and `ship_date` to pandas datetime with `dayfirst=True`."
        )
    ]
    with open(notebooks_dir / "02_data_cleaning.ipynb", "w", encoding="utf-8") as f:
        nbf.write(nb2, f)

    # 3. 03_feature_engineering.ipynb
    nb3 = make_nb()
    nb3.cells = [
        nbf.v4.new_markdown_cell(
            "# 03. Feature Engineering & Domain Enrichment\n"
            "**Project:** Global Retail Business Analytics & Decision Intelligence  \n"
            "**Author:** Muhammad Awais Bacha | Devixo Solutions  \n\n"
            "### Objectives:\n"
            "- Engineer temporal dimensions (year, month, quarter, transit days)\n"
            "- Derive financial margins, unit costs, and profitability indicators\n"
            "- Aggregate customer lifetime statistics and order-level totals."
        ),
        nbf.v4.new_code_cell(
            "import pandas as pd\n"
            "from src.data.load_data import load_raw_dataset\n"
            "from src.data.clean_data import clean_dataset\n"
            "from src.data.feature_engineering import engineer_features\n\n"
            "df_raw = load_raw_dataset()\n"
            "df_clean, _ = clean_dataset(df_raw)\n"
            "df_feat, meta = engineer_features(df_clean)\n\n"
            "print(f'Transformed feature space: {meta[\"initial_features\"]} -> {meta[\"final_features\"]} columns')\n"
            "print('New features:', meta['engineered_feature_names'])\n"
            "df_feat[['order_id', 'sales', 'profit', 'profit_margin_pct', 'unit_price', 'shipping_duration_days']].head(5)"
        )
    ]
    with open(notebooks_dir / "03_feature_engineering.ipynb", "w", encoding="utf-8") as f:
        nbf.write(nb3, f)

    # 4. 04_exploratory_data_analysis.ipynb
    nb4 = make_nb()
    nb4.cells = [
        nbf.v4.new_markdown_cell(
            "# 04. Exploratory Data Analysis & Visualizations\n"
            "**Project:** Global Retail Business Analytics & Decision Intelligence  \n"
            "**Author:** Muhammad Awais Bacha | Devixo Solutions  \n\n"
            "### Objectives:\n"
            "- Analyze transaction distributions, seasonality, and regional volume\n"
            "- Evaluate category and subcategory profitability\n"
            "- Discover discount threshold impact on margins."
        ),
        nbf.v4.new_code_cell(
            "import pandas as pd\n"
            "from pathlib import Path\n"
            "from src.visualization.create_visualizations import generate_all_visualizations\n\n"
            "df = pd.read_csv('data/processed/cleaned_global_superstore.csv')\n"
            "output_dir = Path('reports/figures')\n"
            "saved_figs = generate_all_visualizations(df, output_dir)\n"
            "print(f'Successfully validated {len(saved_figs)} visualization figures in {output_dir}')"
        )
    ]
    with open(notebooks_dir / "04_exploratory_data_analysis.ipynb", "w", encoding="utf-8") as f:
        nbf.write(nb4, f)

    # 5. 05_business_analysis.ipynb
    nb5 = make_nb()
    nb5.cells = [
        nbf.v4.new_markdown_cell(
            "# 05. Business Analysis & KPI Calculations\n"
            "**Project:** Global Retail Business Analytics & Decision Intelligence  \n"
            "**Author:** Muhammad Awais Bacha | Devixo Solutions  \n\n"
            "### Objectives:\n"
            "- Calculate and audit the 7 core executive KPIs\n"
            "- Perform annual and regional performance breakdowns\n"
            "- Synthesize actionable business insights and strategic initiatives."
        ),
        nbf.v4.new_code_cell(
            "import pandas as pd\n"
            "from src.analysis.kpi_calculations import calculate_overall_kpis, calculate_yearly_kpis, calculate_category_kpis\n\n"
            "df = pd.read_csv('data/processed/cleaned_global_superstore.csv')\n"
            "overall_kpis = calculate_overall_kpis(df)\n"
            "yearly_kpis = calculate_yearly_kpis(df)\n"
            "cat_kpis = calculate_category_kpis(df)\n\n"
            "print('Executive KPI Summary:')\n"
            "for k, v in overall_kpis.items():\n"
            "    print(f'  {k}: {v}')\n\n"
            "print('\\nYearly KPI Trends:')\n"
            "print(yearly_kpis[['order_year', 'total_revenue', 'total_profit', 'revenue_growth_pct', 'profit_margin_pct']])\n\n"
            "print('\\nCategory Performance:')\n"
            "print(cat_kpis[['category', 'revenue', 'profit', 'profit_margin_pct', 'revenue_share_pct']])"
        )
    ]
    with open(notebooks_dir / "05_business_analysis.ipynb", "w", encoding="utf-8") as f:
        nbf.write(nb5, f)

    # 6. 06_machine_learning.ipynb
    nb6 = make_nb()
    nb6.cells = [
        nbf.v4.new_markdown_cell(
            "# 06. Machine Learning: Demand Forecasting & Customer Segmentation\n"
            "**Project:** Global Retail Business Analytics & Decision Intelligence  \n"
            "**Author:** Muhammad Awais Bacha | Devixo Solutions  \n\n"
            "### Objectives:\n"
            "- Model A: Time-Series Demand Forecasting (Random Forest vs Naive/Moving Average)\n"
            "- Model B: Customer RFM Segmentation via K-Means Clustering\n"
            "- Evaluate models with rigorous metrics (MAE, RMSE, MAPE, Silhouette Score)."
        ),
        nbf.v4.new_code_cell(
            "from pathlib import Path\n"
            "import pandas as pd\n"
            "from src.models.sales_forecasting import prepare_monthly_series, train_and_evaluate_forecasting\n"
            "from src.models.customer_segmentation import build_rfm_features, run_customer_segmentation\n\n"
            "df = pd.read_csv('data/processed/cleaned_global_superstore.csv')\n\n"
            "# 1. Sales Forecasting\n"
            "monthly = prepare_monthly_series(df)\n"
            "forecast_metrics, pred_df = train_and_evaluate_forecasting(monthly, test_months=12)\n"
            "print('Sales Forecasting Benchmark Metrics:')\n"
            "for model, metrics in forecast_metrics.items():\n"
            "    print(f'  {model}: {metrics}')\n\n"
            "# 2. Customer Segmentation\n"
            "rfm = build_rfm_features(df)\n"
            "rfm_labeled, profiles, eval_meta = run_customer_segmentation(rfm, n_clusters=4)\n"
            "print(f'\\nCustomer Segmentation (Silhouette={eval_meta[\"silhouette_score\"]:.3f}):')\n"
            "print(profiles[['segment_name', 'customer_count', 'avg_recency', 'avg_monetary', 'revenue_share_pct']])"
        )
    ]
    with open(notebooks_dir / "06_machine_learning.ipynb", "w", encoding="utf-8") as f:
        nbf.write(nb6, f)

    print("All 6 Jupyter notebooks built successfully in:", notebooks_dir)


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parents[1]
    create_all_notebooks(base_dir / "notebooks")
