from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from scipy.stats import zscore

from src.reports.tearsheet import load_data
from src.analytics.clustering import impute_sector_median
BASE_DIR = Path(__file__).resolve().parents[2]

OUTPUT_DIR = BASE_DIR / "output"
REPORT_DIR = OUTPUT_DIR / "reports"

CLUSTER_FEATURES = [

    "return_on_equity_pct",

    "debt_to_equity",

    "revenue_cagr_5yr",

    "free_cash_flow_cr",

    "operating_profit_margin_pct",
]

KPI_COLUMNS = [

    "return_on_equity_pct",

    "return_on_assets_pct",

    "return_on_capital_employed_pct",

    "debt_to_equity",

    "interest_coverage",

    "asset_turnover",

    "revenue_cagr_5yr",

    "operating_profit_margin_pct",

    "net_profit_margin_pct",

    "free_cash_flow_cr",
]

def latest_snapshot(df):

    df = df[df["year"] != "TTM"].copy()

    df["year_dt"] = pd.to_datetime(
        df["year"],
        format="%b %Y",
        errors="coerce"
    )

    return (
        df.sort_values("year_dt")
          .groupby("company_id")
          .tail(1)
          .drop(columns="year_dt")
          .reset_index(drop=True)
    )

def load_clusters():

    return pd.read_csv(
        OUTPUT_DIR / "cluster_labels.csv"
    )


def merged_data():

    df = latest_snapshot(load_data())

    df = impute_sector_median(df)

    clusters = load_clusters()

    return df.merge(
        clusters,
        on="company_id",
        how="left"
    )

def profile_clusters(df):

    mean_profile = (
        df.groupby("cluster_id")[CLUSTER_FEATURES]
          .mean()
          .round(2)
    )

    median_profile = (
        df.groupby("cluster_id")[CLUSTER_FEATURES]
          .median()
          .round(2)
    )

    print("\nCluster Mean Profile")
    print(mean_profile)

    print("\nCluster Median Profile")
    print(median_profile)

    return mean_profile, median_profile

def correlation_heatmap(df):

    corr = df[KPI_COLUMNS].corr(method="pearson")

    plt.figure(figsize=(10,8))

    sns.heatmap(
        corr,
        annot=True,
        cmap="coolwarm",
        fmt=".2f"
    )

    plt.title("Correlation Heatmap")

    plt.tight_layout()

    plt.savefig(
        REPORT_DIR / "correlation_heatmap.png",
        dpi=300
    )

    plt.close()

    print("Saved correlation_heatmap.png")

def detect_outliers(df):

    df = df.copy()

    flags = pd.Series(False, index=df.index)

    for col in KPI_COLUMNS:

        z = (
            df.groupby("broad_sector")[col]
              .transform(
                lambda x: (
                    np.zeros(len(x))
                    if x.fillna(x.median()).std(ddof=0) == 0
                    else zscore(
                        x.fillna(x.median()),
                        nan_policy="omit"
                    )
                )
              )
        )

        flags |= (np.abs(z) > 3)

    outliers = df.loc[flags]

    outliers.to_csv(
        OUTPUT_DIR / "outlier_report.csv",
        index=False
    )

    print(f"Outliers: {len(outliers)}")

    return outliers

def portfolio_statistics(df):

    stats = []

    for col in KPI_COLUMNS:

        s = df[col].dropna()

        stats.append({

            "Metric": col,

            "P10": s.quantile(0.10),

            "P25": s.quantile(0.25),

            "P50": s.quantile(0.50),

            "P75": s.quantile(0.75),

            "P90": s.quantile(0.90),

            "Mean": s.mean(),

            "Std": s.std()
        })

    stats = pd.DataFrame(stats).round(2)

    stats.to_csv(
        OUTPUT_DIR / "portfolio_stats.csv",
        index=False
    )

    print("Saved portfolio_stats.csv")
    
def main():

    df = merged_data()

    mean_profile, median_profile = profile_clusters(df)

    correlation_heatmap(df)

    detect_outliers(df)

    portfolio_statistics(df)

    print("=" * 60)
    print("Day 37 Analytics Completed Successfully")
    print("=" * 60)


if __name__ == "__main__":
    main()

