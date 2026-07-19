import streamlit as st
import pandas as pd

from utils.db import (
    get_companies,
    get_company_ratios
)

companies = get_companies()

company = st.selectbox(
    "Select Company",
    companies["id"]
)

df = get_company_ratios(company)

if df.empty:
    st.warning("No data available.")
    st.stop()

df = df[df["year"] != "TTM"].copy()

df["sort_year"] = (
    df["year"]
    .str.extract(r"(\d{4})")
    .astype(int)
)

df = df.sort_values("sort_year")

latest = df.iloc[-1]

score = 0

if latest["roe_percentage"] >= 15:
    score += 2

if latest["roce_percentage"] >= 15:
    score += 2

if latest["debt_to_equity"] < 1:
    score += 2

if latest["revenue_cagr_5yr"] > 10:
    score += 2

if latest["interest_coverage"] > 5:
    score += 2

st.subheader("⭐ Overall Quality Score")

st.progress(score / 10)

st.metric(
    "Investment Score",
    f"{score}/10"
)

strengths = []

if latest["roe_percentage"] >= 15:
    strengths.append("High Return on Equity")

if latest["roce_percentage"] >= 15:
    strengths.append("Strong Return on Capital")

if latest["debt_to_equity"] < 1:
    strengths.append("Low Debt")

if latest["free_cash_flow_cr"] > 0:
    strengths.append("Positive Free Cash Flow")

if latest["interest_coverage"] > 5:
    strengths.append("Strong Interest Coverage")

st.subheader("✅ Strengths")

for s in strengths:
    st.write("•", s)

weaknesses = []

if latest["debt_to_equity"] >= 1:
    weaknesses.append("High Debt")

if latest["interest_coverage"] <= 5:
    weaknesses.append("Weak Interest Coverage")

if latest["free_cash_flow_cr"] < 0:
    weaknesses.append("Negative Free Cash Flow")

if latest["asset_turnover"] < 1:
    weaknesses.append("Low Asset Utilization")

st.subheader("⚠️ Weaknesses")

if weaknesses:
    for w in weaknesses:
        st.write("•", w)
else:
    st.success("No major weaknesses identified.")

metrics = pd.DataFrame({
    "Metric": [
        "ROE",
        "ROCE",
        "Revenue CAGR",
        "PAT CAGR",
        "Debt/Equity",
        "Interest Coverage",
        "Free Cash Flow"
    ],
    "Value": [
        latest["roe_percentage"],
        latest["roce_percentage"],
        latest["revenue_cagr_5yr"],
        latest["pat_cagr_5yr"],
        latest["debt_to_equity"],
        latest["interest_coverage"],
        latest["free_cash_flow_cr"]
    ]
})

st.subheader("📊 Key Financial Metrics")
st.dataframe(metrics, use_container_width=True)


if score >= 9:
    rating = "⭐⭐⭐⭐⭐ Excellent"
elif score >= 7:
    rating = "⭐⭐⭐⭐ Very Good"
elif score >= 5:
    rating = "⭐⭐⭐ Average"
else:
    rating = "⭐⭐ Needs Improvement"

st.subheader(f"Overall Rating: {rating}")




