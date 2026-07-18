import streamlit as st
import plotly.express as px

from utils.db import (
    get_sectors,
    get_latest_ratios
)
import streamlit as st
from utils.db import get_latest_ratios, get_companies

latest = get_latest_ratios()
companies = get_companies()

st.write("Latest Ratios Columns")
st.write(latest.columns.tolist())

st.write("Companies Columns")
st.write(companies.columns.tolist())
st.set_page_config(
    page_title="Sector Analysis",
    page_icon="🏭",
    layout="wide"
)

st.title("🏭 Sector Analysis")

ratios = get_latest_ratios()

sectors = sorted(
    ratios["broad_sector"].dropna().unique()
)

selected_sector = st.selectbox(
    "Select Sector",
    sectors
)

sector_df = ratios[
    ratios["broad_sector"] == selected_sector
].copy()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Companies",
    len(sector_df)
)

col2.metric(
    "Average ROE",
    f"{sector_df['roe_percentage'].mean():.2f}%"
)

col3.metric(
    "Average ROCE",
    f"{sector_df['roce_percentage'].mean():.2f}%"
)

col4.metric(
    "Average Revenue CAGR",
    f"{sector_df['revenue_cagr_5yr'].mean():.2f}%"
)
top_roe = (
    sector_df
    .sort_values(
        "roe_percentage",
        ascending=False
    )
)

fig = px.bar(
    top_roe,
    x="company_id",
    y="roe_percentage",
    title="🏆 ROE Comparison",
    text="roe_percentage"
)

fig.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside"
)

fig.update_layout(
    coloraxis_showscale=False
)

st.plotly_chart(
    fig,
    use_container_width=True
)
fig = px.bar(
    top_roe,
    x="company_id",
    y="roce_percentage",
    color="roce_percentage",
    title="🏭 ROCE Comparison"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
fig = px.bar(
    top_roe,
    x="company_id",
    y="revenue_cagr_5yr",
    color="revenue_cagr_5yr",
    title="📈 Revenue CAGR (5 Years)"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
fig = px.bar(
    top_roe,
    x="company_id",
    y="debt_to_equity",
    color="debt_to_equity",
    title="💳 Debt to Equity"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

with st.expander("📋 Sector Data"):

    st.dataframe(
        sector_df,
        use_container_width=True
    )

    st.download_button(
        "Download CSV",
        sector_df.to_csv(index=False),
        "sector_analysis.csv",
        "text/csv"
    )
col1, col2 = st.columns(2)

ranking = (
    sector_df[
        [
            "company_id",
            "roe_percentage",
            "roce_percentage",
            "revenue_cagr_5yr",
            "debt_to_equity"
        ]
    ]
    .sort_values("roe_percentage", ascending=False)
)

st.subheader("🏆 Sector Ranking")

st.dataframe(
    ranking,
    use_container_width=True,
    hide_index=True
)
best = sector_df.loc[
    sector_df["roe_percentage"].idxmax()
]

st.info(
    f"🏆 **{best['company_id']}** has the highest ROE "
    f"({best['roe_percentage']:.2f}%) in the {selected_sector} sector."
)