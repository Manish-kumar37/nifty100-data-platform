import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

conn.close()

import re

def extract_year(year):
    match = re.search(r"\d{4}", str(year))
    return int(match.group()) if match else 0

df["sort_year"] = df["year"].apply(extract_year)

latest = (
    df
    .sort_values("sort_year")
    .groupby("company_id")
    .tail(1)
)

def generate_pros(row):
    pros = []

    if row["return_on_equity_pct"] >= 20:
        pros.append("High return on equity indicates efficient capital utilization.")

    if row["debt_to_equity"] <= 0.5:
        pros.append("Low debt levels reduce financial risk.")

    if row["free_cash_flow_cr"] > 0:
        pros.append("Positive free cash flow supports future growth.")

    if row["interest_coverage"] >= 5:
        pros.append("Strong interest coverage indicates healthy debt servicing.")

    if row["net_profit_margin_pct"] >= 15:
        pros.append("Healthy profit margins reflect operational efficiency.")

    return pros

def generate_cons(row):
    cons = []

    if row["debt_to_equity"] > 1:
        cons.append("High debt levels increase financial risk.")

    if row["free_cash_flow_cr"] < 0:
        cons.append("Negative free cash flow may indicate cash generation issues.")

    if row["interest_coverage"] < 2:
        cons.append("Weak interest coverage suggests repayment pressure.")

    if row["net_profit_margin_pct"] < 5:
        cons.append("Low profit margins may affect long-term profitability.")

    if row["return_on_equity_pct"] < 10:
        cons.append("Low return on equity indicates inefficient capital utilization.")

    return cons    


rows = []

for _, row in latest.iterrows():

    rows.append({
        "company_id": row["company_id"],
        "pros": " | ".join(generate_pros(row)),
        "cons": " | ".join(generate_cons(row))
    })

result = pd.DataFrame(rows)

result.to_csv(
    "output/pros_cons_generated.csv",
    index=False
)

print(f"Generated reports for {len(result)} companies.")    