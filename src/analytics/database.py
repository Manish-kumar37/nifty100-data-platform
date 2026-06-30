"""
SQLite utilities for Ratio Engine
Sprint 2
"""

import sqlite3
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path.cwd()
DB_PATH = PROJECT_ROOT / "nifty100.db"


def create_connection():
    return sqlite3.connect(DB_PATH)


def save_financial_ratios(df):
    """
    Replace financial_ratios table
    with computed KPI dataframe.
    """

    with create_connection() as conn:

        df.to_sql(
            "financial_ratios",
            conn,
            if_exists="replace",
            index=False
        )

    print(
        f"financial_ratios updated: {len(df)} rows"
    )


def load_financial_ratios():

    with create_connection() as conn:

        return pd.read_sql(
            "SELECT * FROM financial_ratios",
            conn
        )