"""
Composite Quality Score
Sprint 2
"""
import numpy as np
import pandas as pd

WEIGHTS = {
    "roe": 0.15,
    "roce": 0.10,
    "npm": 0.10,
    "fcf": 0.20,
    "revenue": 0.15,
    "pat": 0.15,
    "de": 0.10,
    "icr": 0.05,
}

def quality_score(row):

    score = 0

    # Profitability
    if row["return_on_equity_pct"] is not None:
        if row["return_on_equity_pct"] >= 15:
            score += 2
        elif row["return_on_equity_pct"] >= 10:
            score += 1

    # Leverage
    if row["debt_to_equity"] is not None:
        if row["debt_to_equity"] < 1:
            score += 2
        elif row["debt_to_equity"] < 2:
            score += 1

    # Interest Coverage
    if row["interest_coverage"] is not None:
        if row["interest_coverage"] > 3:
            score += 2
        elif row["interest_coverage"] > 1.5:
            score += 1

    # Cash Flow
    if row["free_cash_flow_cr"] is not None:
        if row["free_cash_flow_cr"] > 0:
            score += 2

    # Asset Turnover
    if row["asset_turnover"] is not None:
        if row["asset_turnover"] > 1:
            score += 2

    return score

def winsorize_series(series):
    """
    Cap values between the 10th and 90th percentile
    to reduce the effect of extreme outliers.
    """

    series = pd.to_numeric(series, errors="coerce")

    p10 = series.quantile(0.10)
    p90 = series.quantile(0.90)

    return series.clip(lower=p10, upper=p90)

def normalize_metric(series, inverse=False):
    """
    Normalize a metric to a 0–100 scale.

    inverse=True is used for metrics where
    lower values are better (e.g. Debt/Equity).
    """

    series = winsorize_series(series)

    minimum = series.min()
    maximum = series.max()

    if pd.isna(minimum) or pd.isna(maximum):
        return pd.Series(0, index=series.index)

    if maximum == minimum:
        return pd.Series(50, index=series.index)

    normalized = (
        (series - minimum)
        / (maximum - minimum)
    ) * 100

    if inverse:
        normalized = 100 - normalized
    normalized = normalized.fillna(50)


    return normalized.round(2)

if __name__ == "__main__":

    s = pd.Series([10, 20, 30, 40, 1000])

    print("Original")
    print(s)

    print()

    print("Winsorized")
    print(winsorize_series(s))

    print()

    print("Normalized")
    print(normalize_metric(s))

def calculate_composite_score(df):
    """
    Calculate weighted composite quality score (0–100).
    """

    df = df.copy()

    # Normalize every metric
    df["roe_score"] = normalize_metric(
        df["return_on_equity_pct"]
    )

    df["roce_score"] = normalize_metric(
        df["return_on_capital_employed_pct"]
    )

    df["npm_score"] = normalize_metric(
        df["net_profit_margin_pct"]
    )

    df["fcf_score"] = normalize_metric(
        df["free_cash_flow_cr"]
    )

    df["revenue_score"] = normalize_metric(
        df["revenue_cagr_5yr"]
    )

    df["pat_score"] = normalize_metric(
        df["pat_cagr_5yr"]
    )

    df["de_score"] = normalize_metric(
        df["debt_to_equity"],
        inverse=True
    )

    df["icr_score"] = normalize_metric(
        df["interest_coverage"]
    )
    score_columns = [
    "roe_score",
    "roce_score",
    "npm_score",
    "fcf_score",
    "revenue_score",
    "pat_score",
    "de_score",
    "icr_score",
]

    df[score_columns] = df[score_columns].fillna(50)
    df["composite_quality_score"] = (

        df["roe_score"] * 0.15 +

        df["roce_score"] * 0.10 +

        df["npm_score"] * 0.10 +

        df["fcf_score"] * 0.20 +

        df["revenue_score"] * 0.15 +

        df["pat_score"] * 0.15 +

        df["de_score"] * 0.10 +

        df["icr_score"] * 0.05

    ).round(2)
    df["roe_score"] * WEIGHTS["roe"]
    return df    

def sector_normalize(df):
    """
    Normalize composite score within each broad sector.
    """

    df = df.copy()

    df["sector_quality_score"] = 0.0

    for sector in df["broad_sector"].dropna().unique():

        mask = df["broad_sector"] == sector

        sector_scores = normalize_metric(
            df.loc[mask, "composite_quality_score"]
        )

        df.loc[mask, "sector_quality_score"] = sector_scores

    return df

def add_composite_scores(df):
    """
    Add all quality scores.
    """

    df = calculate_composite_score(df)

    df = sector_normalize(df)

    return df

# if __name__ == "__main__":

#     import sqlite3

#     conn = sqlite3.connect("nifty100.db")

#     df = pd.read_sql(
#         "SELECT * FROM financial_ratios",
#         conn
#     )

#     conn.close()

#     df = add_composite_scores(df)

#     print(
#         df[
#             [
#                 "company_id",
#                 "broad_sector",
#                 "composite_quality_score",
#                 "sector_quality_score"
#             ]
#         ].head(20)
#     )
# print(df["composite_quality_score"].min())
# print(df["composite_quality_score"].max())    