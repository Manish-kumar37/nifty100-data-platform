"""
Sprint 5 - Day 32
Capital Allocation Report
"""

from pathlib import Path
import sqlite3
import re

import pandas as pd

DB_FILE = "nifty100.db"

OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)


def load_data():

    conn = sqlite3.connect(DB_FILE)

    df = pd.read_sql(
        "SELECT * FROM financial_ratios",
        conn
    )

    conn.close()

    return df


def extract_year(year):

    match = re.search(r"\d{4}", str(year))

    return int(match.group()) if match else 0


def latest_snapshot(df):

    temp = df.copy()

    temp["sort_year"] = temp["year"].apply(extract_year)

    latest = (
        temp
        .sort_values("sort_year")
        .groupby("company_id")
        .tail(1)
    )

    return latest


def company_history(df, company_id):

    temp = df[
        df["company_id"] == company_id
    ].copy()

    temp["sort_year"] = temp["year"].apply(extract_year)

    temp = temp.sort_values("sort_year")

    return temp

def verify_capital_allocation(df):

    print("=" * 50)
    print("Capital Allocation Verification")
    print("=" * 50)

    companies = df["company_id"].nunique()

    rows = len(df)

    missing = df["capital_allocation"].isna().sum()

    print(f"Companies : {companies}")
    print(f"Rows      : {rows}")
    print(f"Missing   : {missing}")

    return missing == 0

def pattern_distribution(latest):

    distribution = (
        latest["capital_allocation"]
        .value_counts()
        .reset_index()
    )

    distribution.columns = [
        "capital_allocation",
        "company_count"
    ]

    distribution.to_csv(
        OUTPUT_DIR / "capital_allocation_distribution.csv",
        index=False
    )

    return distribution

def pattern_changes(df):

    rows = []

    companies = sorted(
        df["company_id"].unique()
    )

    for company in companies:

        history = company_history(df, company)

        if len(history) < 2:
            continue

        previous = history.iloc[-2]

        latest = history.iloc[-1]

        if (
            previous["capital_allocation"]
            !=
            latest["capital_allocation"]
        ):

            rows.append({

                "company_id": company,

                "previous_year": previous["year"],

                "latest_year": latest["year"],

                "previous_pattern":
                    previous["capital_allocation"],

                "latest_pattern":
                    latest["capital_allocation"]

            })

    changes = pd.DataFrame(rows)

    changes.to_csv(
        OUTPUT_DIR / "pattern_changes.csv",
        index=False
    )

    return changes

def main():

    df = load_data()

    latest = latest_snapshot(df)

    verify = verify_capital_allocation(df)

    distribution = pattern_distribution(latest)

    changes = pattern_changes(df)

    print()

    print("=" * 50)
    print("Distribution Summary")
    print("=" * 50)

    print(distribution)

    print()

    print(f"Pattern Changes : {len(changes)}")

    print()

    if verify:

        print("Verification Passed ✓")

    else:

        print("Verification Failed")

    print("=" * 50)


if __name__ == "__main__":
    main()