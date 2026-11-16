"""
Customer segmentation module for Global Retail Superstore.
Executes RFM (Recency, Frequency, Monetary) feature extraction,
applies K-Means clustering, evaluates cluster silhouette scores,
and generates cluster profiling summaries and visualizations.
"""

from pathlib import Path
from typing import Dict, Any, Tuple
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def build_rfm_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute customer-level Recency, Frequency, and Monetary metrics.
    Reference date is set to one day following the final transaction date.
    """
    df = df.copy()
    if not pd.api.types.is_datetime64_any_dtype(df["order_date"]):
        df["order_date"] = pd.to_datetime(df["order_date"], dayfirst=True)
        
    reference_date = df["order_date"].max() + pd.Timedelta(days=1)
    
    rfm = df.groupby("customer_id").agg(
        recency=("order_date", lambda x: (reference_date - x.max()).days),
        frequency=("order_id", "nunique"),
        monetary=("sales", "sum"),
        profit=("profit", "sum"),
        customer_name=("customer_name", "first")
    ).reset_index()
    
    rfm["monetary"] = rfm["monetary"].round(2)
    rfm["profit"] = rfm["profit"].round(2)
    return rfm


def run_customer_segmentation(
    rfm_df: pd.DataFrame,
    n_clusters: int = 4,
    output_dir: Optional[Path] = None
) -> Tuple[pd.DataFrame, pd.DataFrame, Dict[str, Any]]:
    """
    Scales RFM metrics, performs K-Means clustering, and derives segment profiles.
    """
    rfm_data = rfm_df[["recency", "frequency", "monetary"]].copy()
    
    # Apply log1p transformation to mitigate severe monetary skew
    rfm_log = np.log1p(rfm_data)
    scaler = StandardScaler()
    rfm_scaled = scaler.fit_transform(rfm_log)
    
    # Calculate Silhouette score
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(rfm_scaled)
    sil_score = silhouette_score(rfm_scaled, cluster_labels)
    
    rfm_df = rfm_df.copy()
    rfm_df["cluster"] = cluster_labels
    
    # Profile clusters
    profile = rfm_df.groupby("cluster").agg(
        customer_count=("customer_id", "count"),
        avg_recency=("recency", "mean"),
        avg_frequency=("frequency", "mean"),
        avg_monetary=("monetary", "mean"),
        total_revenue=("monetary", "sum"),
        avg_profit=("profit", "mean")
    ).reset_index()
    
    total_rev = rfm_df["monetary"].sum()
    profile["revenue_share_pct"] = ((profile["total_revenue"] / total_rev) * 100).round(2)
    profile["avg_recency"] = profile["avg_recency"].round(1)
    profile["avg_frequency"] = profile["avg_frequency"].round(1)
    profile["avg_monetary"] = profile["avg_monetary"].round(2)
    profile["avg_profit"] = profile["avg_profit"].round(2)
    profile["total_revenue"] = profile["total_revenue"].round(2)

    # Assign business labels based on empirical centroids
    # Sort by avg_monetary descending to map standardized business names
    sorted_clusters = profile.sort_values(by="avg_monetary", ascending=False)["cluster"].tolist()
    label_map = {
        sorted_clusters[0]: "Champions (High-Value Loyal)",
        sorted_clusters[1]: "Core Growth Customers",
        sorted_clusters[2]: "Occasional Shoppers",
        sorted_clusters[3]: "At-Risk / Lapsed Customers"
    }
    rfm_df["segment_name"] = rfm_df["cluster"].map(label_map)
    profile["segment_name"] = profile["cluster"].map(label_map)
    profile = profile.sort_values(by="total_revenue", ascending=False).reset_index(drop=True)
    
    logger.info(f"Segmentation finished (k={n_clusters}, Silhouette={sil_score:.3f}):")
    for _, row in profile.iterrows():
        logger.info(f"  {row['segment_name']}: {row['customer_count']} customers, Avg Spend: ${row['avg_monetary']:,.2f}, Share: {row['revenue_share_pct']}%")
        
    # Visualization
    if output_dir:
        output_dir.mkdir(parents=True, exist_ok=True)
        fig, ax = plt.subplots(figsize=(9, 6))
        palette = {"Champions (High-Value Loyal)": "#2ca02c", "Core Growth Customers": "#1f77b4", "Occasional Shoppers": "#ff7f0e", "At-Risk / Lapsed Customers": "#d62728"}
        
        for name, group in rfm_df.groupby("segment_name"):
            ax.scatter(group["recency"], group["monetary"], label=name, color=palette.get(name, "grey"), alpha=0.7, s=40)
            
        ax.set_title(f"Customer RFM Segmentation (k={n_clusters}, Silhouette Score: {sil_score:.2f})")
        ax.set_xlabel("Recency (Days Since Last Order)")
        ax.set_ylabel("Monetary Value ($ Total Spend)")
        ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("${x:,.0f}"))
        ax.legend(title="Customer Segment", loc="upper right")
        
        plot_path = output_dir / "customer_segments_scatter.png"
        fig.savefig(plot_path, dpi=300, bbox_inches="tight")
        plt.close(fig)
        logger.info(f"Saved segmentation plot to {plot_path}")
        
        # Save profiles CSV
        profile_path = output_dir / "customer_segment_profiles.csv"
        profile.to_csv(profile_path, index=False)
        
    eval_info = {
        "n_clusters": n_clusters,
        "silhouette_score": round(float(sil_score), 3),
        "total_customers": len(rfm_df)
    }
    return rfm_df, profile, eval_info


if __name__ == "__main__":
    from src.data.load_data import load_raw_dataset
    from src.data.clean_data import clean_dataset
    
    base_dir = Path(__file__).resolve().parents[2]
    df_raw = load_raw_dataset()
    df_clean, _ = clean_dataset(df_raw)
    rfm = build_rfm_features(df_clean)
    
    out_dir = base_dir / "models" / "customer_segmentation"
    rfm_labeled, profiles, eval_meta = run_customer_segmentation(rfm, n_clusters=4, output_dir=out_dir)
    print("\nSegment Profiles:")
    print(profiles[["segment_name", "customer_count", "avg_recency", "avg_frequency", "avg_monetary", "revenue_share_pct"]])
