"""
Pros & Cons Generator
Sprint 5 - Day 30
"""
"""
Sprint 5 – Day 30
Automatic Pros & Cons Generator

Input:
    financial_ratios table

Output:
    output/pros_cons_generated.csv

Generates:
    - 12 Pro rules
    - 12 Con rules
    - Confidence score
"""
from pathlib import Path
import sqlite3

import pandas as pd

from src.nlp.rules import PRO_RULES, CON_RULES, make_rule
from src.nlp.utils import (
    latest_snapshot,
    company_history
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


def apply_rules(company, history):

    records = []
    pro_results = []
    con_results = []
    history_rules = {
        "rule_pr10",
        "rule_pr12",
        "rule_cr08",
        "rule_cr09"
    }

    for rule in PRO_RULES:

        if rule.__name__ in history_rules:
            result = rule(history)
        else:
            result = rule(company)

        if result:
            result["company_id"] = company["company_id"]
            records.append(result)

    for rule in CON_RULES:

        if rule.__name__ in history_rules:
            result = rule(history)
        else:
            result = rule(company)

        if result:
            result["company_id"] = company["company_id"]
            records.append(result)
    

        # Fallback Pro
        if not pro_results:
            pro_results.append(
                make_rule(
                    "pro",
                    "PR99",
                    "Business has stable operations despite not triggering major quantitative strengths.",
                    50,
                )
            )

        # Fallback Con
        if not con_results:
            con_results.append(
                make_rule(
                    "con",
                    "CR99",
                    "Monitor valuation, competition, and future growth expectations despite strong fundamentals.",
                    50,
                )
            )

    for result in pro_results + con_results:
        result["company_id"] = company["company_id"]
        records.append(result)
    return records


def generate(df):

    latest = latest_snapshot(df)

    rows = []

    for _, company in latest.iterrows():

        history = company_history(
            df,
            company["company_id"]
        )

        rows.extend(
            apply_rules(
                company,
                history
            )
        )

    return pd.DataFrame(rows)


def validate(output_df, companies):

    pro = set(output_df[output_df["type"] == "pro"]["company_id"])
    con = set(output_df[output_df["type"] == "con"]["company_id"])

    missing = []

    for company in companies:

        has_pro = company in pro
        has_con = company in con

        if not has_pro or not has_con:
            missing.append({
                "company_id": company,
                "has_pro": has_pro,
                "has_con": has_con
            })

    return pd.DataFrame(missing)


def save(df):

    output = OUTPUT_DIR / "pros_cons_generated.csv"

    df.to_csv(
        output,
        index=False
    )

    print(f"Saved: {output}")


def main():

    df = load_data()

    result = generate(df)

    save(result)

    latest = latest_snapshot(df)

    missing = validate(result, latest["company_id"])

    # print(missing)

    missing.to_csv(
        "output/missing_rules.csv",
        index=False
    )

    print()

    print("=" * 40)
    print(f"Companies        : {len(latest)}")
    print(f"Rules Generated  : {len(result)}")
    print(f"Missing Companies: {len(missing)}")

    if not missing.empty:
        print("Missing:")
        print(missing)
    else:
        print("Validation Passed ✓")

    print("=" * 40)


if __name__ == "__main__":
    main()