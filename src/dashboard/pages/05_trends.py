import streamlit as st
import pandas as pd
import plotly.express as px

from utils.db import (
    get_companies,
    get_company_ratios
)
st.set_page_config(
    page_title="Company Trends",
    page_icon="📈",
    layout="wide"
)
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
st.title("📈 Company Trends")
companies = get_companies()

selected_company = st.selectbox(
    "Select Company",
    companies["id"]
)
df = get_company_ratios(selected_company)

if df.empty:
    st.warning("No historical data available.")
    st.stop()   

df = df[df["year"] != "TTM"].copy()

df["sort_year"] = (
    df["year"]
    .str.extract(r"(\d{4})")
    .astype(int)
)

df = df.sort_values("sort_year")

with st.expander("📋 View Historical Financial Data"):
    st.dataframe(df, use_container_width=True)
first = df.iloc[0]
latest = df.iloc[-1]

def growth(first_value, latest_value):
    if first_value == 0:
        return 0
    return ((latest_value - first_value) / first_value) * 100

rev_growth = growth(first["sales"], latest["sales"])
profit_growth = growth(first["net_profit"], latest["net_profit"])
latest = df.iloc[-1]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Revenue",
        f"₹ {latest['sales']:,.0f} Cr",
        f"{rev_growth:.1f}%"
    )

with col2:
    st.metric(
        "Net Profit",
        f"₹ {latest['net_profit']:,.0f} Cr",
        f"{profit_growth:.1f}%"
    )

with col3:
    st.metric(
        "Operating Margin",
        f"{latest['opm_percentage']:.1f}%"
    )

with col4:
    st.metric(
        "Operating Profit",
        f"₹ {latest['operating_profit']:,.0f} Cr"
    )

revenue_fig = px.line(
    df,
    x="year",
    y="sales",
    markers=True,
    title="📈 Revenue Trend"
)

revenue_fig = style_chart(revenue_fig)



profit_fig = px.line(
    df,
    x="year",
    y="net_profit",
    markers=True,
    title="💰 Net Profit Trend"
)

profit_fig = style_chart(profit_fig)

op_fig = px.line(
    df,
    x="year",
    y="operating_profit",
    markers=True,
    title="⚙️ Operating Profit Trend"
)

op_fig = style_chart(op_fig)

expense_fig = px.bar(
    df,
    x="year",
    y="expenses",
    title="💸 Expenses"
)

expense_fig = style_chart(expense_fig)

compare = df.melt(
    id_vars="year",
    value_vars=["sales", "expenses"],
    var_name="Metric",
    value_name="Value"
)

compare_fig = px.line(
    compare,
    x="year",
    y="Value",
    color="Metric",
    markers=True,
    title="📊 Revenue vs Expenses"
)

compare_fig = style_chart(compare_fig)

row1_col1, row1_col2 = st.columns(2)

with row1_col1:
    st.plotly_chart(revenue_fig, use_container_width=True)

with row1_col2:
    st.plotly_chart(profit_fig, use_container_width=True)

row2_col1, row2_col2 = st.columns(2)

with row2_col1:
    st.plotly_chart(compare_fig, use_container_width=True)

with row2_col2:
    st.plotly_chart(op_fig, use_container_width=True)

st.plotly_chart(expense_fig, use_container_width=True)

st.subheader("📌 Trend Summary")

summary = []

# Revenue Growth
if rev_growth > 20:
    summary.append("📈 Revenue has grown significantly over the available historical period.")
elif rev_growth > 0:
    summary.append("📈 Revenue has shown steady positive growth.")
else:
    summary.append("📉 Revenue has declined over the available historical period.")

# Net Profit Growth
if profit_growth > 20:
    summary.append("💰 Net profit has increased strongly, indicating improved profitability.")
elif profit_growth > 0:
    summary.append("💰 Net profit has grown steadily.")
else:
    summary.append("⚠️ Net profit has declined.")

# Operating Margin
if latest["opm_percentage"] >= 20:
    summary.append("⚙️ Operating margin is healthy, suggesting efficient operations.")
elif latest["opm_percentage"] >= 10:
    summary.append("⚙️ Operating margin is moderate.")
else:
    summary.append("⚠️ Operating margin is relatively low.")

# Operating Profit
if latest["operating_profit"] > first["operating_profit"]:
    summary.append("📊 Operating profit has improved over the years.")
else:
    summary.append("📊 Operating profit has weakened over the years.")

# Display summary
for point in summary:
    st.write(point)