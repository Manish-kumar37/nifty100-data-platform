import streamlit as st

from utils.db import (
    get_companies,
    get_company_info,
    get_company_ratios
)

st.title("🏢 Company Profile")

companies = get_companies()

company_list = sorted(companies["id"].unique())

selected = st.selectbox(
    "Select Company",
    company_list
)

info = get_company_info(selected).iloc[0]

st.markdown("---")

st.subheader(info["company_name"])

col1, col2 = st.columns([2, 1])

with col1:

    st.markdown(f"**🌐 Website:** {info['website']}")

    st.markdown("### 📖 About")
    st.write(info["about_company"])

with col2:

    st.metric("Face Value", info["face_value"])
    st.metric("Book Value", info["book_value"])
    st.metric("ROE %", info["roe_percentage"])
    st.metric("ROCE %", info["roce_percentage"])

st.markdown("---")

company_data = get_company_ratios(selected)
st.write(company_data.columns.tolist())
latest = (
    company_data[company_data["year"] != "TTM"]
    .sort_values("year")
    .iloc[-1]
)

st.subheader("📊 Financial Highlights")

c1, c2, c3 = st.columns(3)

with c1:
    st.metric("ROE", f"{latest['roe_percentage']:.2f}%")

with c2:
    st.metric("ROCE", f"{latest['roce_percentage']:.2f}%")

with c3:
    st.metric("Debt / Equity", f"{latest['debt_to_equity']:.2f}")

c4, c5, c6 = st.columns(3)

with c4:
    st.metric(
        "Profit Margin",
        f"{latest['net_profit_margin_pct']:.2f}%"
    )

with c5:
    st.metric(
        "Revenue CAGR (5Y)",
        f"{latest['revenue_cagr_5yr']:.2f}%"
    )

with c6:
    st.metric(
        "Free Cash Flow",
        f"{latest['free_cash_flow_cr']:.2f} Cr"
    )

with st.expander("📋 View Financial Data"):
    st.dataframe(company_data, use_container_width=True)  

import plotly.express as px
#net profit vs revenue
chart_data = (
    company_data[company_data["year"] != "TTM"]
    .sort_values("year")
)

fig = px.line(
    chart_data,
    x="year",
    y=["sales", "net_profit"],
    markers=True,
    title="Revenue vs Net Profit"
)

st.plotly_chart(fig, use_container_width=True)


st.subheader("📈 Revenue vs Net Profit Trend")

chart_data = (
    company_data[company_data["year"] != "TTM"]
    .copy()
)

# Extract the 4-digit year
chart_data["sort_year"] = (
    chart_data["year"]
    .str.extract(r"(\d{4})")
    .astype(int)
)

chart_data = chart_data.sort_values("sort_year")

fig = px.line(
    chart_data,
    x="year",
    y=["sales", "net_profit"],
    markers=True,
    labels={
        "value": "₹ Crore",
        "year": "Financial Year",
        "variable": "Metric"
    }
)

fig.update_layout(
    height=450,
    legend_title="",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)
st.write(chart_data[["year", "sales", "net_profit"]])

st.markdown("---")
st.subheader("📈 Growth Analysis")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("### Revenue CAGR")
    st.metric("3 Years", f"{latest['revenue_cagr_3yr']:.2f}%")
    st.metric("5 Years", f"{latest['revenue_cagr_5yr']:.2f}%")
    st.metric("10 Years", f"{latest['revenue_cagr_10yr']:.2f}%")

with c2:
    st.markdown("### PAT CAGR")
    st.metric("3 Years", f"{latest['pat_cagr_3yr']:.2f}%")
    st.metric("5 Years", f"{latest['pat_cagr_5yr']:.2f}%")
    st.metric("10 Years", f"{latest['pat_cagr_10yr']:.2f}%")

with c3:
    st.markdown("### EPS CAGR")
    st.metric("3 Years", f"{latest['eps_cagr_3yr']:.2f}%")
    st.metric("5 Years", f"{latest['eps_cagr_5yr']:.2f}%")
    st.metric("10 Years", f"{latest['eps_cagr_10yr']:.2f}%")

#growth analysis
strengths = []
weaknesses = []

if latest["roe_percentage"] >= 20:
    strengths.append("High Return on Equity")

if latest["roce_percentage"] >= 20:
    strengths.append("Excellent ROCE")

if latest["debt_to_equity"] < 0.5:
    strengths.append("Low Debt")

if latest["free_cash_flow_cr"] > 0:
    strengths.append("Positive Free Cash Flow")

if latest["revenue_cagr_5yr"] > 10:
    strengths.append("Strong Revenue Growth")


if latest["debt_to_equity"] > 1:
    weaknesses.append("High Debt")

if latest["interest_coverage"] < 3:
    weaknesses.append("Low Interest Coverage")

if latest["net_profit_margin_pct"] < 10:
    weaknesses.append("Low Profit Margin")

if latest["revenue_cagr_5yr"] < 5:
    weaknesses.append("Weak Revenue Growth")

#Build Strengths & Weaknesses

st.markdown("---")
st.subheader("🟢 Strengths & 🔴 Weaknesses")

strengths = []
weaknesses = []

# Strengths
if latest["roe_percentage"] >= 20:
    strengths.append("High Return on Equity")

if latest["roce_percentage"] >= 20:
    strengths.append("Excellent Return on Capital")

if latest["debt_to_equity"] < 0.5:
    strengths.append("Low Debt Company")

if latest["free_cash_flow_cr"] > 0:
    strengths.append("Positive Free Cash Flow")

if latest["revenue_cagr_5yr"] > 10:
    strengths.append("Strong Revenue Growth")

# Weaknesses
if latest["debt_to_equity"] > 1:
    weaknesses.append("High Debt")

if latest["interest_coverage"] < 3:
    weaknesses.append("Low Interest Coverage")

if latest["net_profit_margin_pct"] < 10:
    weaknesses.append("Low Profit Margin")

if latest["revenue_cagr_5yr"] < 5:
    weaknesses.append("Slow Revenue Growth")

left, right = st.columns(2)

with left:
    st.success("Strengths")
    if strengths:
        for item in strengths:
            st.write(f"✅ {item}")
    else:
        st.write("No major strengths detected.")

with right:
    st.warning("Weaknesses")
    if weaknesses:
        for item in weaknesses:
            st.write(f"⚠️ {item}")
    else:
        st.write("No major weaknesses detected.")


st.markdown("---")
st.subheader("💰 Cash Flow Trend")

cashflow = (
    company_data[company_data["year"] != "TTM"]
    .copy()
)

cashflow["sort_year"] = (
    cashflow["year"]
    .str.extract(r"(\d{4})")
    .astype(int)
)

cashflow = cashflow.sort_values("sort_year")
fig = px.bar(
    cashflow,
    x="year",
    y=[
        "operating_activity",
        "investing_activity",
        "financing_activity"
    ],
    barmode="group",
    labels={
        "value": "₹ Crore",
        "year": "Financial Year",
        "variable": "Cash Flow"
    },
    title="Operating vs Investing vs Financing Cash Flow"
)

fig.update_layout(
    height=500,
    legend_title="",
    xaxis_title="Financial Year",
    yaxis_title="₹ Crore",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)
st.markdown(
    f"🌐 **Website:** [{info['website']}]({info['website']})"
)
st.image(info["company_logo"], width=120)