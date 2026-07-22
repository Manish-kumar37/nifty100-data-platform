"""
Portfolio Report Generator
Sprint 5 - Day 34
"""

from pathlib import Path

import pandas as pd

INPUT_FILE = "reports/tearsheets/company_tearsheets.xlsx"

OUTPUT_DIR = Path("reports/portfolio")

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)
def load_data():

    return pd.read_excel(INPUT_FILE)

def top_picks(df):

    return (
        df
        .sort_values(
            ["cashflow_score", "roe"],
            ascending=False
        )
        .head(10)
    )

def growth_leaders(df):

    return (
        df
        .sort_values(
            ["revenue_cagr", "pat_cagr"],
            ascending=False
        )
        .head(10)
    )

def quality_leaders(df):

    quality = df[
        (df["roe"] >= 20) &
        (df["debt_to_equity"] <= 1)
    ]

    return (
        quality
        .sort_values(
            "roe",
            ascending=False
        )
        .head(10)
    )

def distress_watchlist(df):

    return (
        df[df["rating"] == "Weak"]
        .sort_values(
            "cashflow_score"
        )
    )

def portfolio_summary(df):

    summary = pd.DataFrame({

        "Metric": [

            "Companies",

            "Excellent",

            "Good",

            "Average",

            "Weak"

        ],

        "Value": [

            len(df),

            (df["rating"] == "Excellent").sum(),

            (df["rating"] == "Good").sum(),

            (df["rating"] == "Average").sum(),

            (df["rating"] == "Weak").sum()

        ]

    })

    return summary

def save_report(
    top,
    growth,
    quality,
    distress,
    summary
):

    output = OUTPUT_DIR / "portfolio_report.xlsx"

    with pd.ExcelWriter(output) as writer:

        top.to_excel(
            writer,
            sheet_name="Top Picks",
            index=False
        )

        growth.to_excel(
            writer,
            sheet_name="Growth Leaders",
            index=False
        )

        quality.to_excel(
            writer,
            sheet_name="Quality Leaders",
            index=False
        )

        distress.to_excel(
            writer,
            sheet_name="Distress Watchlist",
            index=False
        )

        summary.to_excel(
            writer,
            sheet_name="Portfolio Summary",
            index=False
        )

    print(f"Saved: {output}")

def main():

    df = load_data()

    top = top_picks(df)

    growth = growth_leaders(df)

    quality = quality_leaders(df)

    distress = distress_watchlist(df)

    summary = portfolio_summary(df)

    save_report(
        top,
        growth,
        quality,
        distress,
        summary
    )

    print("Portfolio Report Generated Successfully")


if __name__ == "__main__":
    main()    