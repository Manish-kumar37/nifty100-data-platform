"""
Cash Flow Intelligence
Sprint 5 - Day 31
"""

import re
import sqlite3
from pathlib import Path

import pandas as pd

from src.analytics.cashflow_kpis import (
    calculate_free_cash_flow,
    calculate_cfo_quality,
    calculate_capex_intensity,
    calculate_fcf_conversion,
    capital_allocation_pattern,
)

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

    if match:
        return int(match.group())

    return 0    


def latest_snapshot(df):

    df["sort_year"] = df["year"].apply(extract_year)

    df = df[df["sort_year"] != 0]

    latest = (
        df
        .sort_values("sort_year")
        .groupby("company_id")
        .tail(1)
    )

    return latest


def detect_distress(row):

    alerts = []

    if row["operating_activity"] < 0:
        alerts.append("Negative Operating Cash Flow")

    if row["free_cash_flow_cr"] < 0:
        alerts.append("Negative Free Cash Flow")

    if row["interest_coverage"] < 2:
        alerts.append("Weak Interest Coverage")

    if row["debt_to_equity"] > 2:
        alerts.append("High Debt")

    return alerts

def detect_pattern(values):

    if len(values) < 3:
        return "Insufficient Data"

    values = values[-3:]

    if values[0] < values[1] < values[2]:
        return "Improving"

    if values[0] > values[1] > values[2]:
        return "Deteriorating"

    spread = max(values) - min(values)

    if spread > abs(sum(values) / len(values)):
        return "Volatile"

    return "Stable"

def calculate_score(row):

    score = 0

    if row["operating_activity"] > 0:
        score += 2

    if row["free_cash_flow_cr"] > 0:
        score += 2

    if row["debt_to_equity"] < 1:
        score += 2

    if row["interest_coverage"] > 5:
        score += 2

    if row["roe_percentage"] > 20:
        score += 2

    return score

def get_rating(score):

    if score >= 9:
        return "Excellent"

    if score >= 7:
        return "Good"

    if score >= 5:
        return "Average"

    return "Weak"


def company_history(df, company_id):

    history = (
        df[df["company_id"] == company_id]
        .sort_values("sort_year")
    )

    return history

def main():

    df = load_data()
    # print(df.columns.tolist())
    # return
    df["sort_year"] = df["year"].apply(extract_year)
    df = df[df["sort_year"] != 0]

    latest = latest_snapshot(df)

    intelligence = []
    distress = []
    patterns = []

    for _, row in latest.iterrows():

        company = row["company_id"]

        history = company_history(df, company)

        # ---------- KPIs ----------

        fcf = calculate_free_cash_flow(
            row["operating_activity"],
            row["investing_activity"]
        )

        cfo_quality = calculate_cfo_quality(
            row["operating_activity"],
            row["net_profit"]
        )

        capex = calculate_capex_intensity(
            row["investing_activity"],
            row["sales"]
        )

        fcf_conversion = calculate_fcf_conversion(
            fcf,
            row["operating_profit"]
        )

        allocation = capital_allocation_pattern(
            row["operating_activity"],
            row["investing_activity"],
            row["financing_activity"],
            cfo_quality
        )

        # ---------- Distress ----------

        alerts = detect_distress(row)

        for alert in alerts:
            distress.append({
                "company_id": company,
                "alert": alert
            })

        # ---------- Pattern ----------

        pattern = detect_pattern(
            history["operating_activity"].tolist()
        )

        patterns.append({
            "company_id": company,
            "pattern": pattern
        })

        # ---------- Score ----------

        score = calculate_score(row)

        rating = get_rating(score)

        intelligence.append({

            "company_id": company,

            "free_cash_flow": fcf,

            "cfo_quality": cfo_quality,

            "capex_intensity": capex,

            "fcf_conversion": fcf_conversion,

            "capital_allocation": allocation,

            "cashflow_score": score,

            "rating": rating

        })

    print(f"Processed {len(latest)} companies")
    intelligence_df = pd.DataFrame(intelligence)
    distress_df = pd.DataFrame(distress)
    patterns_df = pd.DataFrame(patterns)
    distress_df.to_csv(
        OUTPUT_DIR / "distress_alerts.csv",
        index=False
    )

    patterns_df.to_csv(
        OUTPUT_DIR / "pattern_changes.csv",
        index=False
    )
    with pd.ExcelWriter(
        OUTPUT_DIR / "cashflow_intelligence.xlsx"
    ) as writer:

        intelligence_df.to_excel(
            writer,
            sheet_name="Intelligence",
            index=False
        )

        distress_df.to_excel(
            writer,
            sheet_name="Distress",
            index=False
        )

        patterns_df.to_excel(
            writer,
            sheet_name="Patterns",
            index=False
        )
    print()

    print("Cash Flow Intelligence Generated Successfully")

    print(f"Companies Analysed : {len(intelligence_df)}")
    print(f"Distress Alerts    : {len(distress_df)}")
    print(f"Pattern Records    : {len(patterns_df)}")
if __name__ == "__main__":
    main()    