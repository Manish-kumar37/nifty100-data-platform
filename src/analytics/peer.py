"""
Sprint 3 - Day 18
Peer Percentile Engine
"""

import sqlite3
import pandas as pd

DB_PATH = "nifty100.db"


def load_data():
    """
    Load financial ratios and peer groups.
    """

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
    """
    Keep latest annual record.
    """

    df = df[df["year"] != "TTM"].copy()

    df["sort_year"] = (
        df["year"]
        .str.extract(r"(\d{4})")
        .astype(float)
    )

    df = (
        df.sort_values("sort_year")
          .groupby("company_id")
          .tail(1)
          .drop(columns="sort_year")
    )

    return df

def merge_peer_groups(ratios, peers):
    """
    Merge latest financial ratios with peer group information.
    """

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

METRICS = {
    "return_on_equity_pct": False,
    "return_on_capital_employed_pct": False,
    "net_profit_margin_pct": False,
    "debt_to_equity": True,
    "free_cash_flow_cr": False,
    "pat_cagr_5yr": False,
    "revenue_cagr_5yr": False,
    "eps_cagr_5yr": False,
    "interest_coverage": False,
    "asset_turnover": False
}
def percentile_rank(series, inverse=False):
    """
    Calculate percentile ranks.
    """

    rank = series.rank(
        pct=True,
        method="average"
    )

    if inverse:
        rank = 1 - rank

    return (rank * 100).round(2)

def compute_peer_percentiles(df):

    results = []

    for peer_group, group in df.groupby(
        "peer_group_name",
        dropna=False
    ):

        if pd.isna(peer_group):

            print(
                f"{len(group)} companies have no peer group assigned."
            )

            continue

        if pd.isna(peer_group):
            continue

        for metric, inverse in METRICS.items():

            scores = percentile_rank(
                group[metric],
                inverse=inverse
            )

            temp = pd.DataFrame({

                "company_id":
                    group["company_id"],

                "peer_group_name":
                    peer_group,

                "metric":
                    metric,

                "value":
                    group[metric],

                "percentile_rank":
                    scores,

                "year":
                    group["year"]

            })

            results.append(temp)

    return pd.concat(
        results,
        ignore_index=True
    )

def save_percentiles(df):

    conn = sqlite3.connect(DB_PATH)

    df.to_sql(
        "peer_percentiles",
        conn,
        if_exists="replace",
        index=False
    )

    conn.close()

if __name__ == "__main__":

    ratios, peers = load_data()

    ratios = latest_records(ratios)

    merged = merge_peer_groups(
        ratios,
        peers
    )

    result = compute_peer_percentiles(
        merged
    )

    save_percentiles(result)
    conn = sqlite3.connect(DB_PATH)

    count = pd.read_sql(
        "SELECT COUNT(*) AS total FROM peer_percentiles",
        conn
    )

    conn.close()

    print()

    print(count)
    

    print("Peer percentile table created.")

    print("Rows:", len(result))

    print()

    print(result.head(10))