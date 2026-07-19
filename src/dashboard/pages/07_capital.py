import streamlit as st
import plotly.express as px

from utils.db import (
    get_companies,
    get_company_ratios
)
companies = get_companies()
def style_chart(fig):
    fig.update_layout(
        template="plotly_dark",
        height=420,
        title_x=0.5,
        hovermode="x unified",
        margin=dict(
            l=20,
            r=20,
            t=60,
            b=20
        ),
        legend_title="",
        font=dict(size=14)
    )

    fig.update_xaxes(
        showgrid=False
    )

    fig.update_yaxes(
        showgrid=True
    )

    return fig
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

col1,col2,col3,col4 = st.columns(4)

col1.metric(
    "Free Cash Flow",
    f"₹ {latest['free_cash_flow_cr']:,.0f} Cr"
)

col2.metric(
    "Debt / Equity",
    f"{latest['debt_to_equity']:.2f}"
)

col3.metric(
    "Interest Coverage",
    f"{latest['interest_coverage']:.2f}"
)

col4.metric(
    "Asset Turnover",
    f"{latest['asset_turnover']:.2f}"
)
score = latest["capital_allocation"]

score = latest["capital_allocation"]

st.subheader("💰 Capital Allocation")

if score == "Excellent":
    st.success(f"🟢 {score}")
elif score == "Good":
    st.info(f"🔵 {score}")
elif score == "Average":
    st.warning(f"🟡 {score}")
else:
    st.error(f"🔴 {score}")

fcf_fig = px.line(
    df,
    x="year",
    y="free_cash_flow_cr",
    markers=True,
    title="💰 Free Cash Flow"
)

fcf_fig = style_chart(fcf_fig)

debt_fig = px.line(
    df,
    x="year",
    y="debt_to_equity",
    markers=True,
    title="🏦 Debt to Equity"
)

debt_fig = style_chart(debt_fig)
interest_fig = px.line(
    df,
    x="year",
    y="interest_coverage",
    markers=True,
    title="📈 Interest Coverage"
)

interest_fig = style_chart(interest_fig)
asset_fig = px.line(
    df,
    x="year",
    y="asset_turnover",
    markers=True,
    title="🏭 Asset Turnover"
)

asset_fig = style_chart(asset_fig)
    

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fcf_fig, use_container_width=True)

with col2:
    st.plotly_chart(debt_fig, use_container_width=True)

col3, col4 = st.columns(2)

with col3:
    st.plotly_chart(interest_fig, use_container_width=True)

with col4:
    st.plotly_chart(asset_fig, use_container_width=True)

with st.expander("📋 Historical Capital Allocation Data"):
    st.dataframe(df, use_container_width=True)    

st.subheader("📌 Financial Health Summary")

summary = []

# Free Cash Flow
if latest["free_cash_flow_cr"] > 0:
    summary.append("💰 Positive free cash flow indicates healthy cash generation.")
else:
    summary.append("⚠️ Negative free cash flow may indicate pressure on liquidity.")

# Debt
if latest["debt_to_equity"] < 1:
    summary.append("🏦 Debt levels are comfortably managed.")
else:
    summary.append("⚠️ Debt-to-equity ratio is relatively high.")

# Interest Coverage
if latest["interest_coverage"] > 5:
    summary.append("📈 Earnings comfortably cover interest obligations.")
else:
    summary.append("⚠️ Interest coverage is relatively weak.")

# Asset Turnover
if latest["asset_turnover"] > 1:
    summary.append("🏭 Assets are being utilized efficiently.")
else:
    summary.append("ℹ️ Asset utilization could be improved.")

# Capital Allocation
summary.append(f"🎯 Capital Allocation Rating: {latest['capital_allocation']}")

for point in summary:
    st.write(point)
if latest["asset_turnover"] > 1:
    st.success("✅ Assets are being utilized efficiently.")
else:
    st.info("ℹ️ Asset utilization has room for improvement.")

st.write(df["capital_allocation"].unique())    