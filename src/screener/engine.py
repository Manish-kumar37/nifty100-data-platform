"""
Sprint 3 - Day 15
Financial Screener Engine
"""

import sqlite3
import pandas as pd
import yaml
from src.analytics.scoring import add_composite_scores

DB_PATH = "nifty100.db"
import os

print(os.path.abspath(DB_PATH))

def load_financial_ratios():
    """
    Load financial_ratios table from SQLite.
    """
    
    conn = sqlite3.connect(DB_PATH)

    df = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    conn.close()

    return df


def load_config(config_path):
    """
    Load screener YAML configuration.
    """

    with open(config_path, "r") as file:

        config = yaml.safe_load(file)

    return config


def apply_filters(df, filters):

    filtered = df.copy()

    print("Initial:", len(filtered))

    for key, value in filters.items():

        if key == "roe_min":
            filtered = filtered[
                filtered["return_on_equity_pct"] >= value
            ]
            print("After ROE:", len(filtered))

        elif key == "debt_to_equity_max":
            filtered = filtered[
                (
                    filtered["broad_sector"] == "Financials"
                )
                |
                (
                    filtered["debt_to_equity"] <= value
                )
            ]
            print("After D/E:", len(filtered))

        elif key == "free_cash_flow_min":
            filtered = filtered[
                filtered["free_cash_flow_cr"] >= value
            ]
            print("After FCF:", len(filtered))

        elif key == "revenue_cagr_5yr_min":
            filtered = filtered[
                filtered["revenue_cagr_5yr"] >= value
            ]
            print("After Revenue CAGR:", len(filtered))

    return filtered.sort_values(
        "composite_quality_score",
        ascending=False
    )

def latest_company_records(df):
    """
    Keep the latest annual financial record for each company.
    Ignore TTM rows because many derived ratios are unavailable.
    """

    df = df.copy()

    # Remove TTM rows
    df = df[df["year"] != "TTM"].copy()

    def year_sort(value):
        try:
            return int(str(value).split()[-1])
        except Exception:
            return 0

    df["sort_year"] = df["year"].apply(year_sort)

    df = (
        df.sort_values(["company_id", "sort_year"])
          .groupby("company_id", as_index=False)
          .tail(1)
          .drop(columns="sort_year")
    )

    return df
def run_screener(preset_name):
    """
    Run a screener preset.
    """

    # Load data
    df = load_financial_ratios()
    print(df["return_on_equity_pct"].count())
    # Add composite scores
    df = add_composite_scores(df)

    # Keep only latest record of each company
    df = latest_company_records(df)

    # Load screener config
    config = load_config(
        "config/screener_config.yaml"
    )

    filters = config[preset_name]
    print("\nTop Calculated ROE")
    print(
        df[
            ["company_id", "return_on_equity_pct"]
        ]
        .sort_values(
            "return_on_equity_pct",
            ascending=False
        )
        .head(15)
    )

    print("\nTop Analysis ROE")
    print(
        df[
            ["company_id", "roe_percentage"]
        ]
        .sort_values(
            "roe_percentage",
            ascending=False
        )
        .head(15)
    )
    print("\nCalculated ROE")
    print(df["return_on_equity_pct"].describe())

    print("\nAnalysis ROE")
    print(df["roe_percentage"].describe())
    # Apply filters on latest records
    result = apply_filters(
        df,
        filters
    )

    return result


if __name__ == "__main__":

    result = run_screener(
        "quality_compounder"
    )

    print()

    print("Companies Found:", len(result))

    print()

    print(
        result[
            [
                "company_id",
                "year",
                "return_on_equity_pct",
                "debt_to_equity",
                "free_cash_flow_cr",
                "revenue_cagr_5yr"
            ]
        ].head(20)
    )

# df = load_financial_ratios()
# print(df.columns.tolist())    

