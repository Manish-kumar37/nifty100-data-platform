import streamlit as st
# from utils.db import (
#     get_latest_ratios,
#     get_peer_comparison
# )
# st.title("🤝 Peer Comparison")
# st.subheader("📋 Peer Companies")
# companies = sorted(
#     get_latest_ratios()["company_id"].unique()
# )

# company = st.selectbox(
#     "Select Company",
#     companies
# )

# peer_df = get_peer_comparison(company)

# st.dataframe(
#     peer_df[
#         [
#             "company_id",
#             "roe_percentage",
#             "roce_percentage",
#             "debt_to_equity",
#             "revenue_cagr_5yr",
#             "net_profit_margin_pct",
#             "free_cash_flow_cr"
#         ]
#     ],
#     use_container_width=True,
#     hide_index=True
# )

# import plotly.express as px

# fig = px.bar(
#     peer_df,
#     x="company_id",
#     y="roe_percentage",
#     color="roe_percentage",
#     title="ROE Comparison"
# )

# st.plotly_chart(
#     fig,
#     use_container_width=True
# )

# fig = px.bar(
#     peer_df,
#     x="company_id",
#     y="revenue_cagr_5yr",
#     color="revenue_cagr_5yr",
#     title="Revenue CAGR (5Y)"
# )

# st.plotly_chart(
#     fig,
#     use_container_width=True
# )

# best = peer_df.sort_values(
#     "roe_percentage",
#     ascending=False
# ).iloc[0]

# st.success(
#     f"🏆 Highest ROE: {best['company_id']} "
#     f"({best['roe_percentage']:.2f}%)"
# )
# companies = sorted(
#     get_latest_ratios()["company_id"].unique()
# )

# selected_company = st.selectbox(
#     "Select Company",
#     companies
# )

# peer_df = get_peer_comparison(selected_company)
# peer_df["Benchmark"] = peer_df["is_benchmark"].map(
#     {
#         1: "🏆 Benchmark",
#         0: ""
#     }
# )   

from utils.db import (
    get_latest_ratios,
    get_peer_comparison
)
companies = sorted(
    get_latest_ratios()["company_id"].unique()
)

selected_company = st.selectbox(
    "Select Company",
    companies
)

peer_df, peer_group = get_peer_comparison(selected_company)

st.info(f"📂 Peer Group: {peer_group}")
st.subheader("📋 Peer Companies")
st.write(peer_df.columns.tolist())
peer_df, peer_group = get_peer_comparison(selected_company)

if peer_df.empty:
    st.warning("No peer group available for this company.")
    st.stop()

st.info(f"📂 Peer Group: {peer_group}")

if len(peer_df) == 1:
    st.info("This company has no comparable peers in the current Nifty 100 dataset.")

peer_df["Benchmark"] = peer_df["is_benchmark"].map({
    1: "🏆 Benchmark",
    0: ""
})
st.write(peer_df.columns)

display = peer_df[
    [
        "company_id",
        "Benchmark",
        "roe_percentage",
        "roce_percentage",
        "debt_to_equity",
        "revenue_cagr_5yr",
        "net_profit_margin_pct",
        "free_cash_flow_cr"
    ]
].rename(columns={
    "company_id": "Company",
    "roe_percentage": "ROE %",
    "roce_percentage": "ROCE %",
    "debt_to_equity": "Debt/Equity",
    "revenue_cagr_5yr": "Revenue CAGR (5Y)",
    "net_profit_margin_pct": "Net Margin %",
    "free_cash_flow_cr": "Free Cash Flow (Cr)"
})

st.dataframe(display, use_container_width=True, hide_index=True)

import plotly.express as px

fig = px.bar(
    peer_df,
    x="company_id",
    y="roe_percentage",
    color="company_id",
    text="roe_percentage",
    title="ROE Comparison"
)

fig.update_traces(textposition="outside")

st.plotly_chart(
    fig,
    use_container_width=True
)
st.write("Selected Company:", selected_company)
st.write("Peer Group:", peer_group)
st.write(peer_df)