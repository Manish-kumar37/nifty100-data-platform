"""
Sprint 5 – Day 31
Cash Flow Intelligence Engine

Input:
    financial_ratios table

Outputs:
    output/cashflow_intelligence.xlsx
    output/distress_alerts.csv
"""

from pathlib import Path
import sqlite3

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

import re


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

def calculate_cfo_quality(history):

    history = history.tail(5)

    ratios = []

    for _, row in history.iterrows():

        pat = row["net_profit"]

        cfo = row["operating_activity"]

        if pd.isna(pat):
            continue

        if pat <= 0:
            continue

        ratios.append(cfo / pat)

    if not ratios:

        return 0, "Insufficient Data"

    score = round(sum(ratios) / len(ratios), 2)

    if score > 1:

        label = "High Quality"

    elif score >= 0.5:

        label = "Moderate"

    else:

        label = "Accrual Risk"

    return score, label

def calculate_capex_intensity(company):

    sales = company["sales"]

    capex = abs(company["investing_activity"])

    if pd.isna(sales) or sales == 0:

        return 0, "Unknown"

    pct = round(
        capex / sales * 100,
        2
    )

    if pct < 3:

        label = "Asset Light"

    elif pct <= 8:

        label = "Moderate"

    else:

        label = "Capital Intensive"

    return pct, label

def calculate_distress(company):

    return bool(
        company["operating_activity"] < 0
        and
        company["financing_activity"] > 0
    )

def calculate_deleveraging(history):

    if len(history) < 2:

        return False

    latest = history.iloc[-1]

    previous = history.iloc[-2]

    return bool(

        latest["financing_activity"] < 0

        and

        latest["borrowings"]
        <
        previous["borrowings"]

    )
def calculate_fcf_cagr(history):

    history = history.tail(5)

    if len(history) < 2:
        return None

    start = history.iloc[0]["free_cash_flow_cr"]
    end = history.iloc[-1]["free_cash_flow_cr"]

    if pd.isna(start) or pd.isna(end):
        return None

    if start <= 0 or end <= 0:
        return None

    years = len(history) - 1

    cagr = ((end / start) ** (1 / years) - 1) * 100

    return round(cagr, 2)

def calculate_fcf_conversion(company):

    pat = company["net_profit"]
    fcf = company["free_cash_flow_cr"]

    if pd.isna(pat) or pat <= 0:
        return None

    return round((fcf / pat) * 100, 2)

def capital_allocation_label(company):

    value = company["capital_allocation"]

    if pd.isna(value):
        return "Unknown"

    return str(value)





def main():

    df = load_data()

    latest = latest_snapshot(df)

    rows = []

    for _, company in latest.iterrows():

        history = company_history(df, company["company_id"])

        cfo_score, cfo_label = calculate_cfo_quality(history)

        capex_pct, capex_label = calculate_capex_intensity(company)

        rows.append({
            "company_id": company["company_id"],
            "sector": company["broad_sector"],
            "cfo_quality_score": cfo_score,
            "cfo_quality_label": cfo_label,
            "capex_intensity_pct": capex_pct,
            "capex_label": capex_label,
            "fcf_cagr_5yr": calculate_fcf_cagr(history),
            "fcf_conversion_pct": calculate_fcf_conversion(company),
            "distress_flag": calculate_distress(company),
            "deleveraging_flag": calculate_deleveraging(history),
            "capital_allocation_label": capital_allocation_label(company),
        })

    result = pd.DataFrame(rows)

    result.to_excel(
        OUTPUT_DIR / "cashflow_intelligence.xlsx",
        index=False,
    )

    alerts = latest[
        (latest["operating_activity"] < 0)
        &
        (latest["financing_activity"] > 0)
    ][[
        "company_id",
        "operating_activity",
        "financing_activity",
        "net_profit",
    ]]

    alerts.to_csv(
        OUTPUT_DIR / "distress_alerts.csv",
        index=False,
    )

    print("=" * 40)
    print(f"Companies          : {len(result)}")
    print(f"Distress Alerts    : {len(alerts)}")
    print("Cash Flow Intelligence Generated ✓")
    print("=" * 40)


if __name__ == "__main__":
    main()