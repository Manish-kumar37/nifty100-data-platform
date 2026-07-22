"""
Sector Report Generator
Sprint 5 - Day 33
"""

from pathlib import Path

import pandas as pd
# print("sector_report.py loaded")
INPUT_FILE = "reports/tearsheets/company_tearsheets.xlsx"

OUTPUT_DIR = Path("reports/sector")

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)
def load_data():

    return pd.read_excel(INPUT_FILE)

def sector_summary(df):

    summary = (

        df.groupby("sector")

        .agg(

            companies=("company_id", "count"),

            avg_roe=("roe", "mean"),

            avg_roce=("roce", "mean"),

            avg_debt=("debt_to_equity", "mean"),

            avg_interest=("interest_coverage", "mean")

        )

        .reset_index()

    )

    return summary

def top_companies(df):

    return (

        df.sort_values(
            "cashflow_score",
            ascending=False
        )

        .groupby("sector")

        .head(3)

    )

def growth_leaders(df):

    return (

        df.sort_values(
            "revenue_cagr",
            ascending=False
        )

        .groupby("sector")

        .head(3)

    )

def save_reports(summary, top, growth, ranking):
    output = OUTPUT_DIR / "sector_report.xlsx"

    with pd.ExcelWriter(output) as writer:

        summary.to_excel(
            writer,
            sheet_name="Summary",
            index=False
        )

        top.to_excel(
            writer,
            sheet_name="Top Companies",
            index=False
        )

        growth.to_excel(
            writer,
            sheet_name="Growth Leaders",
            index=False
        )
        ranking.to_excel(
            writer,
            sheet_name="Sector Ranking",
            index=False
        )
    print(f"Saved: {output}")
def sector_ranking(summary):

    ranking = summary.copy()

    ranking["interest_score"] = ranking["avg_interest"].clip(upper=50)

    ranking["overall_score"] = (
        ranking["avg_roe"] * 0.4 +
        ranking["avg_roce"] * 0.3 +
        ranking["interest_score"] * 0.2 -
        ranking["avg_debt"] * 0.1
    )

    ranking = ranking.sort_values(
        "overall_score",
        ascending=False
    )

    return ranking
def main():

    print("Inside main()")

    df = load_data()

    print(df.head())

    summary = sector_summary(df)

    print(summary.head())

    ranking = sector_ranking(summary)

    top = top_companies(df)

    growth = growth_leaders(df)

    save_reports(
        summary,
        top,
        growth,
        ranking
    )

    print("Done!")


if __name__ == "__main__":
    main()    