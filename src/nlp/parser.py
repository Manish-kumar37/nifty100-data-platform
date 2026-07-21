import re
from pathlib import Path

import pandas as pd
import pandas as pd

df = pd.read_excel("data/raw/financial_ratios.xlsx")

print(df.head())
print()
print(df.columns.tolist())
print()
print(df.shape)
INPUT_FILE = Path("data/raw/analysis.xlsx")
OUTPUT_DIR = Path("output")

OUTPUT_DIR.mkdir(exist_ok=True)

PATTERN = re.compile(r"(\d+)\s*Years?:?\s*([-\d.]+)%")

TARGET_COLUMNS = [
    "compounded_sales_growth",
    "compounded_profit_growth",
    "stock_price_cagr",
    "roe",
]

def parse_metric(text):
    if pd.isna(text):
        return None

    text = str(text).strip()

    match = PATTERN.search(text)

    if match:
        return (
            int(match.group(1)),
            float(match.group(2))
        )

    return None

def main():

    df = pd.read_excel(INPUT_FILE, header=1)

    parsed_rows = []
    failed_rows = []

    for _, row in df.iterrows():

        company = row["company_id"]

        for metric in TARGET_COLUMNS:

            parsed = parse_metric(row[metric])

            if parsed:

                years, value = parsed

                parsed_rows.append({
                    "company_id": company,
                    "metric_type": metric,
                    "period_years": years,
                    "value_pct": value
                })

            else:

                failed_rows.append({
                    "company_id": company,
                    "metric_type": metric,
                    "raw_text": row[metric]
                })

    parsed_df = pd.DataFrame(parsed_rows)
    failed_df = pd.DataFrame(failed_rows)

    parsed_df.to_csv(
        OUTPUT_DIR / "analysis_parsed.csv",
        index=False
    )

    failed_df.to_csv(
        OUTPUT_DIR / "parse_failures.csv",
        index=False
    )

    print(f"Parsed rows : {len(parsed_df)}")
    print(f"Failures    : {len(failed_df)}")


if __name__ == "__main__":
    main()


parsed_df = pd.read_csv("output/analysis_parsed.csv")
import sqlite3

conn = sqlite3.connect("nifty100.db")

ratio_df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

conn.close()  

import re

def extract_year(year):
    if pd.isna(year):
        return 0

    match = re.search(r"\d{4}", str(year))
    return int(match.group()) if match else 0


ratio_df["sort_year"] = ratio_df["year"].apply(extract_year)

latest_ratio = (
    ratio_df
    .sort_values("sort_year")
    .groupby("company_id")
    .tail(1)
)

COLUMN_MAP = {
    ("compounded_sales_growth", 3): "revenue_cagr_3yr",
    ("compounded_sales_growth", 5): "revenue_cagr_5yr",
    ("compounded_sales_growth", 10): "revenue_cagr_10yr",

    ("compounded_profit_growth", 3): "pat_cagr_3yr",
    ("compounded_profit_growth", 5): "pat_cagr_5yr",
    ("compounded_profit_growth", 10): "pat_cagr_10yr",
}

divergence = []

for _, row in parsed_df.iterrows():

    key = (row["metric_type"], row["period_years"])

    if key not in COLUMN_MAP:
        continue

    db_column = COLUMN_MAP[key]

    company = latest_ratio[
        latest_ratio["company_id"] == row["company_id"]
    ]

    if company.empty:
            continue    

    computed = company.iloc[0][db_column]

    if pd.isna(computed):
            continue
    parsed = row["value_pct"]

    difference = abs(parsed - computed)

    if difference > 5:
        divergence.append({
            "company_id": row["company_id"],
            "metric": row["metric_type"],
            "period": row["period_years"],
            "parsed": parsed,
            "computed": computed,
            "difference": round(difference, 2),
        })

    divergence_df = pd.DataFrame(divergence)

    divergence_df.to_csv(
        "output/divergence_report.csv",
        index=False
    )

    print(f"Divergences found: {len(divergence_df)}")    