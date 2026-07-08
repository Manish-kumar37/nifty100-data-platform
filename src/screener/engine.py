"""
Sprint 3 - Day 15
Financial Screener Engine
"""

import sqlite3
import pandas as pd
import yaml


DB_PATH = "nifty100.db"


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
    """
    Apply screener filters.
    """

    filtered = df.copy()

    for key, value in filters.items():

        if key == "roe_min":

            filtered = filtered[
                filtered["return_on_equity_pct"] >= value
            ]

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

        elif key == "free_cash_flow_min":

            filtered = filtered[
                filtered["free_cash_flow_cr"] >= value
            ]

        elif key == "revenue_cagr_5yr_min":

            filtered = filtered[
                filtered["revenue_cagr_5yr"] >= value
            ]

        elif key == "pat_cagr_5yr_min":

            filtered = filtered[
                filtered["pat_cagr_5yr"] >= value
            ]

        elif key == "sales_min":

            filtered = filtered[
                filtered["sales"] >= value
            ]
        elif key == "operating_profit_margin_min":

            filtered = filtered[
                filtered["operating_profit_margin_pct"] >= value
            ]

        elif key == "interest_coverage_min":

            filtered = filtered[
                (
                    filtered["interest_coverage"].isna()
                )
                |
                (
                    filtered["interest_coverage"] >= value
                )
            ]

        elif key == "asset_turnover_min":

            filtered = filtered[
                filtered["asset_turnover"] >= value
            ]

        elif key == "net_profit_min":

            filtered = filtered[
                filtered["net_profit"] >= value
            ]

        elif key == "eps_cagr_5yr_min":

            filtered = filtered[
                filtered["eps_cagr_5yr"] >= value
            ]
    return filtered


def run_screener(preset_name):
    """
    Run a screener preset.
    """

    df = load_financial_ratios()

    config = load_config(
        "config/screener_config.yaml"
    )

    filters = config[preset_name]

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

