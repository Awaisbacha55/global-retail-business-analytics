"""
Master execution pipeline for Global Retail Business Analytics & Decision Intelligence.
Executes data preparation, exploratory visualizations, KPI calculations,
machine learning models, Power BI dimensional exports, and PDF report compilation.

Author: Muhammad Awais Bacha
Internship: Devixo Solutions (Task 04)
"""

import sys
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("MasterPipeline")


def run_pipeline():
    logger.info("=" * 70)
    logger.info("STARTING MASTER PIPELINE: GLOBAL RETAIL BUSINESS ANALYTICS")
    logger.info("=" * 70)

    base_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(base_dir))

    # Phase 1: Data Preparation
    logger.info("[1/6] Running Data Preparation Pipeline...")
    from src.data.prepare_data import run_data_preparation
    processed_csv = run_data_preparation()
    logger.info(f"Processed dataset ready at: {processed_csv}")

    # Phase 2: Exploratory Visualizations
    logger.info("[2/6] Generating Visualizations...")
    import pandas as pd
    from src.visualization.create_visualizations import generate_all_visualizations
    df = pd.read_csv(processed_csv)
    fig_dir = base_dir / "reports" / "figures"
    saved_figs = generate_all_visualizations(df, fig_dir)
    logger.info(f"Generated {len(saved_figs)} visualization figures.")

    # Phase 3: KPI Calculations
    logger.info("[3/6] Computing Executive KPIs...")
    from src.analysis.kpi_calculations import calculate_overall_kpis
    kpis = calculate_overall_kpis(df)
    for k, v in kpis.items():
        logger.info(f"  KPI -> {k}: {v}")

    # Phase 4: Machine Learning - Demand Forecasting
    logger.info("[4/6] Training Time-Series Demand Forecasting Model...")
    from src.models.sales_forecasting import prepare_monthly_series, train_and_evaluate_forecasting
    monthly = prepare_monthly_series(df)
    forecast_out = base_dir / "models" / "sales_forecasting"
    forecast_metrics, _ = train_and_evaluate_forecasting(monthly, test_months=12, output_dir=forecast_out)
    logger.info(f"Forecast Model Evaluation: {forecast_metrics['random_forest']}")

    # Phase 5: Machine Learning - Customer Segmentation
    logger.info("[5/6] Executing Customer RFM Segmentation...")
    from src.models.customer_segmentation import build_rfm_features, run_customer_segmentation
    rfm = build_rfm_features(df)
    seg_out = base_dir / "models" / "customer_segmentation"
    _, profiles, seg_meta = run_customer_segmentation(rfm, n_clusters=4, output_dir=seg_out)
    logger.info(f"Segmentation Complete (k=4, Silhouette: {seg_meta['silhouette_score']:.3f})")

    # Phase 6: PDF Report Compilation
    logger.info("[6/6] Generating Final Executive PDF Report...")
    from src.visualization.generate_pdf_report import build_final_pdf_report
    pdf_out = base_dir / "reports" / "final_project_report.pdf"
    build_final_pdf_report(pdf_out, fig_dir)
    logger.info(f"Final Report Compiled Successfully: {pdf_out} ({pdf_out.stat().st_size:,} bytes)")

    logger.info("=" * 70)
    logger.info("MASTER PIPELINE SUCCESSFULLY COMPLETED ALL PHASES!")
    logger.info("=" * 70)


if __name__ == "__main__":
    run_pipeline()
