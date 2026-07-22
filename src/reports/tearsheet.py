"""
Company Tear Sheet Generator
Sprint 5 - Day 32
"""

import sqlite3
from pathlib import Path

import pandas as pd

DB_FILE = "nifty100.db"

OUTPUT_DIR = Path("reports/tearsheets")

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)

def load_ratios():

    conn = sqlite3.connect(DB_FILE)

    df = pd.read_sql(
        """
        SELECT *
        FROM financial_ratios
        """,
        conn
    )

    conn.close()

    return df

import re

def extract_year(year):

    match = re.search(r"\d{4}", str(year))

    if match:
        return int(match.group())

    return 0


def latest_snapshot(df):

    df = df.copy()

    df["sort_year"] = df["year"].apply(extract_year)

    df = df[df["sort_year"] != 0]

    latest = (
        df
        .sort_values("sort_year")
        .groupby("company_id")
        .tail(1)
    )

    return latest

def build_report(row):

    return {

        "company_id": row["company_id"],

        "sector": row["broad_sector"],

        "roe": row["roe_percentage"],

        "roce": row["roce_percentage"],

        "debt_to_equity": row["debt_to_equity"],

        "interest_coverage": row["interest_coverage"],

        "free_cash_flow": row["free_cash_flow_cr"],

        "capital_allocation": row["capital_allocation"],

        "revenue_cagr": row["revenue_cagr_5yr"],

        "pat_cagr": row["pat_cagr_5yr"]

    }    

def generate_reports():

    df = load_ratios()

    latest = latest_snapshot(df)

    reports = []

    for _, row in latest.iterrows():

        reports.append(build_report(row))

    reports_df = pd.DataFrame(reports)

    return reports_df

def save_reports(df):

    output_file = OUTPUT_DIR / "company_tearsheets.xlsx"

    df.to_excel(
        output_file,
        index=False
    )

    print(f"Saved: {output_file}")

def load_pros_cons():

    return pd.read_csv(
        "output/pros_cons_generated.csv"
    )

def load_cashflow():

    return pd.read_excel(
        "output/cashflow_intelligence.xlsx",
        sheet_name="Intelligence"
    )

def generate_summary(row):

    if row["rating"] == "Excellent":
        return (
            "Excellent quality company with "
            "strong profitability, healthy cash flows "
            "and sound capital allocation."
        )

    if row["rating"] == "Good":
        return (
            "Financially healthy company with a few areas "
            "that should be monitored."
        )

    if row["rating"] == "Average":
        return (
            "Mixed financial profile. Investors should "
            "carefully evaluate the risks."
        )

    return (
        "Weak financial profile with multiple risk indicators "
        "requiring detailed analysis."
    )

def main():

    print("Starting Tear Sheet...")

    reports = generate_reports()
    
    pros = load_pros_cons()

    cashflow = load_cashflow()

    reports = reports.merge(
        cashflow,
        on="company_id",
        how="left"
    )

    reports = reports.merge(
        pros,
        on="company_id",
        how="left"
    )
    reports["summary"] = reports.apply(
    generate_summary,
    axis=1
)
    print(reports.head())

    print(f"Generated {len(reports)} company tear sheets")

    save_reports(reports)

    print("Done!")
    pros = pd.read_csv("output/pros_cons_generated.csv")
    print(pros.columns.tolist())
    print(pros.head())

if __name__ == "__main__":
    main()   