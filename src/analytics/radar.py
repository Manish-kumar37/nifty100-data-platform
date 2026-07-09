"""
Sprint 3 - Day 19
Radar Chart Generator
"""

import os
import sqlite3
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.analytics.scoring import add_composite_scores

DB_PATH = "nifty100.db"

OUTPUT_DIR = "reports/radar_charts"

METRICS = [

    "return_on_equity_pct",

    "return_on_capital_employed_pct",

    "net_profit_margin_pct",

    "debt_to_equity",

    "free_cash_flow_cr",

    "pat_cagr_5yr",

    "revenue_cagr_5yr",

    "composite_quality_score"

]

def load_data():

    conn = sqlite3.connect(DB_PATH)

    ratios = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    peers = pd.read_sql(
        "SELECT * FROM peer_groups",
        conn
    )

    conn.close()

    return ratios, peers

def latest_records(df):

    df = df[df["year"] != "TTM"].copy()

    df["sort_year"] = (
        df["year"]
        .str.extract(r"(\d{4})")
        .astype(float)
    )

    df = (
        df
        .sort_values("sort_year")
        .groupby("company_id")
        .tail(1)
        .drop(columns="sort_year")
    )

    return df

def merge_data(ratios, peers):

    return ratios.merge(

        peers[
            [
                "company_id",
                "peer_group_name",
                "is_benchmark"
            ]
        ],

        on="company_id",

        how="left"

    )

def normalize(series):

    minimum = series.min()

    maximum = series.max()

    if minimum == maximum:

        return series * 0

    return (
        (series - minimum)
        /
        (maximum - minimum)
    ) * 100

def normalize_metrics(df):

    df = df.copy()

    for metric in METRICS:

        if metric in df.columns:

            df[metric] = normalize(
                df[metric].fillna(0)
            )

    return df
def plot_radar(company, peer_avg, company_name):
    """
    Generate radar chart for one company.
    """

    labels = METRICS

    values = company.tolist()
    peer_values = peer_avg.tolist()

    # Close the polygon
    values += values[:1]
    peer_values += peer_values[:1]

    angles = np.linspace(
        0,
        2 * np.pi,
        len(labels),
        endpoint=False
    ).tolist()

    angles += angles[:1]

    fig, ax = plt.subplots(
        figsize=(7, 7),
        subplot_kw=dict(polar=True)
    )

    ax.plot(
        angles,
        values,
        linewidth=2,
        label=company_name
    )

    ax.fill(
        angles,
        values,
        alpha=0.25
    )

    ax.plot(
        angles,
        peer_values,
        linestyle="dashed",
        linewidth=2,
        label="Peer Average"
    )

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    ax.set_ylim(0, 100)

    ax.legend(
        loc="upper right"
    )

    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            f"{company_name}_radar.png"
        )
    )

    plt.close()

def generate_all_charts(df):
    """
    Generate radar chart for every company.
    """

    groups = df.groupby("peer_group_name")

    total = 0

    for peer_group, group in groups:

        if pd.isna(peer_group):
            continue

        peer_average = (
            group[METRICS]
            .mean()
        )

        for _, row in group.iterrows():

            plot_radar(
                row[METRICS],
                peer_average,
                row["company_id"]
            )

            total += 1

    print()

    print(f"Generated {total} radar charts.")    
os.makedirs(

    OUTPUT_DIR,

    exist_ok=True

)

if __name__ == "__main__":

    ratios, peers = load_data()
    
    ratios = add_composite_scores(ratios)
    ratios = latest_records(ratios)

    merged = merge_data(
        ratios,
        peers
    )

    merged = normalize_metrics(
        merged
    )

    generate_all_charts(
        merged
    )