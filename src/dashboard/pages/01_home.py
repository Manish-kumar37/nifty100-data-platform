import streamlit as st
import plotly.express as px

from utils.db import (
    get_latest_ratios,
    get_sectors
)

st.title("🏠 Nifty 100 Dashboard")

# -----------------------------
# Load Data
# -----------------------------

ratios = get_latest_ratios()
sectors = get_sectors()

# -----------------------------
# KPI Calculations
# -----------------------------

avg_roe = ratios["return_on_equity_pct"].mean()

avg_roce = ratios["return_on_capital_employed_pct"].mean()

median_de = ratios["debt_to_equity"].median()

median_growth = ratios["revenue_cagr_5yr"].median()

total_companies = len(ratios)

debt_free = (
    ratios["debt_to_equity"] <= 0.1
).sum()

# -----------------------------
# KPI Cards
# -----------------------------

row1 = st.columns(3)

row1[0].metric(
    "Average ROE",
    f"{avg_roe:.2f}%"
)

row1[1].metric(
    "Average ROCE",
    f"{avg_roce:.2f}%"
)

row1[2].metric(
    "Median D/E",
    f"{median_de:.2f}"
)

row2 = st.columns(3)

row2[0].metric(
    "Companies",
    total_companies
)

row2[1].metric(
    "Median Revenue CAGR",
    f"{median_growth:.2f}%"
)

row2[2].metric(
    "Debt Free Companies",
    debt_free
)

st.divider()

# -----------------------------
# Two Column Layout
# -----------------------------

left, right = st.columns([1,1])

# -----------------------------
# Sector Chart
# -----------------------------

with left:

    st.subheader("Sector Distribution")

    sector_summary = (
        sectors.groupby("broad_sector")
        .size()
        .reset_index(name="Companies")
    )

    fig = px.pie(
        sector_summary,
        names="broad_sector",
        values="Companies",
        hole=0.55
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# -----------------------------
# Top Companies
# -----------------------------

with right:

    st.subheader("Top Companies by ROE")

    top = (
        ratios
        .sort_values(
            "return_on_equity_pct",
            ascending=False
        )
        [
            [
                "company_id",
                "return_on_equity_pct",
                "return_on_capital_employed_pct",
                "debt_to_equity"
            ]
        ]
        .head(5)
    )
    top.columns = [
    "Company",
    "ROE %",
    "ROCE %",
    "Debt/Equity"
]
    st.dataframe(
        top,
        use_container_width=True,
        hide_index=True
    )

# st.divider()

# st.subheader("Financial Dataset Preview")

# st.dataframe(
#     ratios,
#     use_container_width=True,
#     hide_index=True
# )

st.divider()
st.subheader("🏆 Top 5 Companies by ROE")    
st.subheader("Dashboard Insights")

col1, col2 = st.columns(2)

with col1:
    st.info(
        f"📊 Total Companies Analysed : {total_companies}"
    )

    st.success(
        f"💰 Debt-Free Companies : {debt_free}"
    )

with col2:
    st.info(
        f"📈 Median Revenue CAGR : {median_growth:.2f}%"
    )

    st.success(
        f"🏆 Best ROE : {top.iloc[0]['ROE %']:.2f}%"
    )

