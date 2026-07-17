import streamlit as st
import pandas as pd
from utils.db import get_latest_ratios

st.set_page_config(page_title="Stock Screener", layout="wide")

st.title("📊 Stock Screener")

df = get_latest_ratios()

df = df[[
    "company_id",
    "broad_sector",
    "roe_percentage",
    "roce_percentage",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "free_cash_flow_cr",
    "net_profit_margin_pct"
]].copy()

st.sidebar.header("Filters")

sector = st.sidebar.selectbox(
    "Sector",
    ["All"] + sorted(df["broad_sector"].dropna().unique().tolist())
)

min_roe = st.sidebar.slider(
    "Minimum ROE (%)",
    0,
    50,
    15
)

max_debt = st.sidebar.slider(
    "Maximum Debt/Equity",
    0.0,
    5.0,
    0.5,
    0.1
)

min_cagr = st.sidebar.slider(
    "Minimum Revenue CAGR (5Y)",
    -20,
    50,
    10
)

filtered = df.copy()

if sector != "All":
    filtered = filtered[
        filtered["broad_sector"] == sector
    ]

filtered = filtered[
    (filtered["roe_percentage"] >= min_roe)
    & (filtered["debt_to_equity"] <= max_debt)
    & (filtered["revenue_cagr_5yr"] >= min_cagr)
]

st.metric(
    "Companies Found",
    len(filtered)
)

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)

def calculate_score(row):
    score = 0

    if row["roe_percentage"] >= 20:
        score += 1

    if row["roce_percentage"] >= 20:
        score += 1

    if row["debt_to_equity"] <= 0.5:
        score += 1

    if row["revenue_cagr_5yr"] >= 10:
        score += 1

    if row["free_cash_flow_cr"] > 0:
        score += 1

    return score

filtered["Score"] = filtered.apply(calculate_score, axis=1)

filtered["Rating"] = filtered["Score"].apply(
    lambda x: "⭐" * x + "☆" * (5 - x)
)

display_df = filtered[[
    "company_id",
    "broad_sector",
    "Rating",
    "roe_percentage",
    "roce_percentage",
    "debt_to_equity",
    "revenue_cagr_5yr",
    "free_cash_flow_cr",
    "net_profit_margin_pct"
]]

display_df = display_df.rename(columns={
    "company_id": "Company",
    "broad_sector": "Sector",
    "roe_percentage": "ROE %",
    "roce_percentage": "ROCE %",
    "debt_to_equity": "Debt/Equity",
    "revenue_cagr_5yr": "Revenue CAGR (5Y)",
    "free_cash_flow_cr": "Free Cash Flow (Cr)",
    "net_profit_margin_pct": "Net Margin %"
})

st.dataframe(
    display_df,
    use_container_width=True,
    hide_index=True
)

search = st.text_input(
    "🔍 Search Company",
    placeholder="Type company name..."
)

if search:
    filtered = filtered[
        filtered["company_id"]
        .str.contains(search, case=False, na=False)
    ]

csv = display_df.to_csv(index=False).encode("utf-8")

st.download_button(
    "⬇️ Download Results",
    csv,
    "stock_screener.csv",
    "text/csv"
)

