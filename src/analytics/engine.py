"""
Ratio Engine
Sprint 2 - Day 12
"""

import sqlite3
from pathlib import Path

import pandas as pd
from src.analytics.database import save_financial_ratios
from src.analytics.reports import (
    save_capital_allocation,
    save_ratio_edge_cases
)
from src.analytics.cashflow_kpis import (
    capital_allocation_pattern
)
from src.analytics.ratios import (
    calculate_net_profit_margin,
    calculate_operating_profit_margin,
    calculate_roe,
    calculate_roce,
    calculate_roa,
    calculate_debt_to_equity,
    calculate_interest_coverage,
    calculate_asset_turnover,
)
from src.analytics.cagr import calculate_cagr

from src.analytics.cashflow_kpis import (
    calculate_free_cash_flow,
)
from src.analytics.validator import (
    clear_log,
    compare_ratio,
    log_edge_case
)
PROJECT_ROOT = Path.cwd()
DB_PATH = PROJECT_ROOT / "nifty100.db"
import os

print(os.path.abspath(DB_PATH))

def create_connection():
    """
    Create SQLite connection.
    """
    return sqlite3.connect(DB_PATH)


def load_tables():
    """
    Load required tables from SQLite.
    """

    conn = create_connection()

    companies = pd.read_sql(
        "SELECT * FROM companies",
        conn
    )

    pnl = pd.read_sql(
        "SELECT * FROM profitandloss",
        conn
    )

    bs = pd.read_sql(
        "SELECT * FROM balancesheet",
        conn
    )

    cf = pd.read_sql(
        "SELECT * FROM cashflow",
        conn
    )

    sectors = pd.read_sql(
        "SELECT * FROM sectors",
        conn
    )

    conn.close()

    return (
        companies,
        pnl,
        bs,
        cf,
        sectors
    )
#Step 2 — Merge the Tables
def build_base_dataframe():
    """
    Merge all core tables into one dataframe.
    """

    companies, pnl, bs, cf, sectors = load_tables()

    df = pnl.merge(
        bs,
        on=["company_id", "year"],
        how="left",
        suffixes=("", "_bs")
    )

    df = df.merge(
        cf,
        on=["company_id", "year"],
        how="left",
        suffixes=("", "_cf")
    )

    df = df.merge(
        sectors[
            [
                "company_id",
                "broad_sector"
            ]
        ],
        on="company_id",
        how="left"
    )

    # Add source ROE and ROCE from companies table
    df = df.merge(
        companies[
            [
                "id",
                "roe_percentage",
                "roce_percentage"
            ]
        ],
        left_on="company_id",
        right_on="id",
        how="left"
    )
    if "id_y" in df.columns:
        df.drop(columns=["id_y"], inplace=True)

    if "id_x" in df.columns:
        df.rename(
            columns={"id_x": "id"},
            inplace=True
        )
    # Remove duplicate id column after merge
    if "id" in df.columns:
        df.drop(columns=["id"], inplace=True)
    print("\nMissing Values")
    print("Net Profit:", df["net_profit"].isna().sum())
    print("Equity Capital:", df["equity_capital"].isna().sum())
    print("Reserves:", df["reserves"].isna().sum())

    print("\nSample")
    print(
        df[
            [
                "company_id",
                "year",
                "net_profit",
                "equity_capital",
                "reserves"
            ]
        ].head(20)
    )
    return df
def calculate_ratios(df):
    """
    Compute financial KPIs for every company-year.
    """
   
    # ----------------------------
    # Profitability
    # ----------------------------

    df["net_profit_margin_pct"] = df.apply(
        lambda r: calculate_net_profit_margin(
            r["net_profit"],
            r["sales"]
        ),
        axis=1
    )

    df["operating_profit_margin_pct"] = df.apply(
        lambda r: calculate_operating_profit_margin(
            r["operating_profit"],
            r["sales"]
        ),
        axis=1
    )

    df["return_on_equity_pct"] = df.apply(
        lambda r: calculate_roe(
            r["net_profit"],
            r["equity_capital"],
            r["reserves"]
        ),
        axis=1
    )

    df["return_on_assets_pct"] = df.apply(
        lambda r: calculate_roa(
            r["net_profit"],
            r["total_assets"]
        ),
        axis=1
    )

    df["return_on_capital_employed_pct"] = df.apply(
        lambda r: calculate_roce(
            r["operating_profit"],
            r["equity_capital"],
            r["reserves"],
            r["borrowings"]
        ),
        axis=1
    )

    # ----------------------------
    # Leverage
    # ----------------------------

    df["debt_to_equity"] = df.apply(
        lambda r: calculate_debt_to_equity(
            r["borrowings"],
            r["equity_capital"],
            r["reserves"]
        ),
        axis=1
    )

    df["interest_coverage"] = df.apply(
        lambda r: calculate_interest_coverage(
            r["operating_profit"],
            r["other_income"],
            r["interest"]
        ),
        axis=1
    )

    df["asset_turnover"] = df.apply(
        lambda r: calculate_asset_turnover(
            r["sales"],
            r["total_assets"]
        ),
        axis=1
    )

    # ----------------------------
    # Cash Flow
    # ----------------------------

    df["free_cash_flow_cr"] = df.apply(
        lambda r: calculate_free_cash_flow(
            r["operating_activity"],
            r["investing_activity"]
        ),
        axis=1
    )

    df["capital_allocation"] = df.apply(
        lambda r: capital_allocation_pattern(
            r["operating_activity"],
            r["investing_activity"],
            r["financing_activity"]
        ),
        axis=1
    )

    # ----------------------------
    # Validation (AFTER calculations)
    # ----------------------------

    for _, row in df.iterrows():

        compare_ratio(
            row["company_id"],
            row["year"],
            row["return_on_equity_pct"],
            row["roe_percentage"],
            "ROE"
        )

        compare_ratio(
            row["company_id"],
            row["year"],
            row["return_on_capital_employed_pct"],
            row["roce_percentage"],
            "ROCE"
        )

        if (
            row["broad_sector"] == "Financials"
            and row["debt_to_equity"] is not None
            and row["debt_to_equity"] > 5
        ):

            log_edge_case(
                f"{row['company_id']} | "
                f"{row['year']} | "
                f"Financial company - High D/E ignored"
            )
    print(df["return_on_equity_pct"].count())
    print(df["return_on_equity_pct"].head(20))
    return df

def calculate_metric_cagr(
    df,
    metric,
    years,
    value_column,
    flag_column
):
    """
    Generic CAGR calculator for any metric.
    """

    grouped = df.groupby("company_id")

    for company, group in grouped:

        group = group.sort_values("year")

        idx = group.index.tolist()

        for i in range(len(group)):

            if i < years:
                continue

            start_value = group.iloc[i - years][metric]
            end_value = group.iloc[i][metric]

            value, flag = calculate_cagr(
                start_value,
                end_value,
                years
            )

            # Debug only for TVSMOTOR PAT 5Y
            # if (
            #     company == "TVSMOTOR"
            #     and metric == "net_profit"
            #     and years == 5
            # ):
            #     print(
            #         f"{group.iloc[i-years]['year']} ({start_value}) "
            #         f"--> "
            #         f"{group.iloc[i]['year']} ({end_value})"
            #     )
            #     print(type(start_value), type(end_value))
            #     print("Returned:", value, flag)

            df.loc[idx[i], value_column] = value
            df.loc[idx[i], flag_column] = flag

    return df
def add_cagr_columns(df):

    df = df.copy()

    # ----------------------------
    # Create all columns FIRST
    # ----------------------------

    # Revenue
    df["revenue_cagr_3yr"] = None
    df["revenue_cagr_3yr_flag"] = None

    df["revenue_cagr_5yr"] = None
    df["revenue_cagr_5yr_flag"] = None

    df["revenue_cagr_10yr"] = None
    df["revenue_cagr_10yr_flag"] = None

    # PAT
    df["pat_cagr_3yr"] = None
    df["pat_cagr_3yr_flag"] = None

    df["pat_cagr_5yr"] = None
    df["pat_cagr_5yr_flag"] = None

    df["pat_cagr_10yr"] = None
    df["pat_cagr_10yr_flag"] = None

    # EPS
    df["eps_cagr_3yr"] = None
    df["eps_cagr_3yr_flag"] = None

    df["eps_cagr_5yr"] = None
    df["eps_cagr_5yr_flag"] = None

    df["eps_cagr_10yr"] = None
    df["eps_cagr_10yr_flag"] = None

    # ----------------------------
    # Revenue
    # ----------------------------

    df = calculate_metric_cagr(
        df,
        "sales",
        3,
        "revenue_cagr_3yr",
        "revenue_cagr_3yr_flag"
    )

    df = calculate_metric_cagr(
        df,
        "sales",
        5,
        "revenue_cagr_5yr",
        "revenue_cagr_5yr_flag"
    )

    df = calculate_metric_cagr(
        df,
        "sales",
        10,
        "revenue_cagr_10yr",
        "revenue_cagr_10yr_flag"
    )

    # ----------------------------
    # PAT
    # ----------------------------

    df = calculate_metric_cagr(
        df,
        "net_profit",
        3,
        "pat_cagr_3yr",
        "pat_cagr_3yr_flag"
    )

    df = calculate_metric_cagr(
        df,
        "net_profit",
        5,
        "pat_cagr_5yr",
        "pat_cagr_5yr_flag"
    )

    df = calculate_metric_cagr(
        df,
        "net_profit",
        10,
        "pat_cagr_10yr",
        "pat_cagr_10yr_flag"
    )

    # ----------------------------
    # EPS
    # ----------------------------

    df = calculate_metric_cagr(
        df,
        "eps",
        3,
        "eps_cagr_3yr",
        "eps_cagr_3yr_flag"
    )

    df = calculate_metric_cagr(
        df,
        "eps",
        5,
        "eps_cagr_5yr",
        "eps_cagr_5yr_flag"
    )

    df = calculate_metric_cagr(
        df,
        "eps",
        10,
        "eps_cagr_10yr",
        "eps_cagr_10yr_flag"
    )

    return df
#Step 3 — Preview the Data
if __name__ == "__main__":
    clear_log()
    df = build_base_dataframe()

    df = calculate_ratios(df)

    df = add_cagr_columns(df)

    save_financial_ratios(df)

    save_capital_allocation(df)

    save_ratio_edge_cases([])

    print(df.head())

    print()

    print("Rows:", len(df))

    print(
    df[
        [
            "company_id",
            "year",
            "revenue_cagr_5yr",
            "pat_cagr_5yr",
            "eps_cagr_5yr"
        ]
    ].tail(20)
)