from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

from src.reports.tearsheet import load_data

BASE_DIR = Path(__file__).resolve().parents[2]

OUTPUT_DIR = BASE_DIR / "output"
REPORT_DIR = OUTPUT_DIR / "reports"

OUTPUT_DIR.mkdir(exist_ok=True)
REPORT_DIR.mkdir(exist_ok=True)

FEATURES = [
    "return_on_equity_pct",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "free_cash_flow_cr",
    "operating_profit_margin_pct",
]

def latest_snapshot(df):

    return (
        df.sort_values("year")
          .groupby("company_id")
          .tail(1)
          .reset_index(drop=True)
    )

def impute_sector_median(df):

    df = df.copy()

    for col in FEATURES:

        df[col] = (
            df.groupby("broad_sector")[col]
              .transform(lambda x: x.fillna(x.median()))
        )

        df[col] = df[col].fillna(df[col].median())

    return df

def scale_features(df):

    scaler = StandardScaler()

    scaled = scaler.fit_transform(df[FEATURES])

    return scaled, scaler

def elbow_plot(X):

    inertia = []

    ks = range(2, 11)

    for k in ks:

        model = KMeans(
            n_clusters=k,
            random_state=42,
            n_init=10
        )

        model.fit(X)

        inertia.append(model.inertia_)

    plt.figure(figsize=(7,5))

    plt.plot(
        ks,
        inertia,
        marker="o"
    )

    plt.xlabel("Number of Clusters")

    plt.ylabel("Inertia")

    plt.title("KMeans Elbow Plot")

    plt.grid(True)

    plt.savefig(
        REPORT_DIR / "elbow_plot.png",
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("Saved elbow_plot.png")


def run_kmeans(df, X):

    model = KMeans(
        n_clusters=5,
        random_state=42,
        n_init=10
    )

    labels = model.fit_predict(X)

    distances = model.transform(X).min(axis=1)

    result = pd.DataFrame({

        "company_id": df["company_id"],

        "cluster_id": labels,

        "distance_from_centroid": distances,
    })

    return result, model   

CLUSTER_NAMES = {

    0: "Cluster 0",

    1: "Cluster 1",

    2: "Cluster 2",

    3: "Cluster 3",

    4: "Cluster 4",
} 

def add_cluster_names(df):

    df["cluster_name"] = df["cluster_id"].map(CLUSTER_NAMES)

    return df

def main():

    df = load_data()
    # df = load_data()

    # print(df.columns.tolist())

    
    df = latest_snapshot(df)

    df = impute_sector_median(df)

    X, scaler = scale_features(df)

    elbow_plot(X)

    result, model = run_kmeans(df, X)

    result = add_cluster_names(result)

    result.to_csv(
        OUTPUT_DIR / "cluster_labels.csv",
        index=False
    )

    print("=" * 60)
    print("Day 36 Completed Successfully")
    print("=" * 60)


if __name__ == "__main__":
    main()