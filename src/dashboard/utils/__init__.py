# """
# Sprint 4 - Day 23
# Home Dashboard
# """
# import streamlit as st

# st.set_page_config(
#     page_title="Nifty 100 Analytics",
#     page_icon="📈",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# st.title("📈 Nifty 100 Analytics Dashboard")

# st.write("Welcome to the Nifty 100 Analytics Dashboard.")

# st.success("Dashboard loaded successfully.")

# # --------------------------------------------------
# # Sidebar
# # --------------------------------------------------

# selected_year = st.sidebar.selectbox(
#     "Financial Year",
#     [
#         "Mar 2019",
#         "Mar 2020",
#         "Mar 2021",
#         "Mar 2022",
#         "Mar 2023",
#         "Mar 2024"
#     ],
#     index=5
# )

# # --------------------------------------------------
# # Load Data
# # --------------------------------------------------

# companies = get_companies()

# ratios = get_all_ratios()

# sectors = get_sectors()

# ratios = ratios[
#     ratios["year"] == selected_year
# ].copy()

# # --------------------------------------------------
# # KPI Calculations
# # --------------------------------------------------

# avg_roe = ratios["return_on_equity_pct"].mean()

# median_de = ratios["debt_to_equity"].median()

# median_growth = ratios["revenue_cagr_5yr"].median()

# debt_free = (
#     ratios["debt_to_equity"] == 0
# ).sum()

# total_companies = len(ratios)

# # --------------------------------------------------
# # KPI Cards
# # --------------------------------------------------

# c1, c2, c3, c4, c5 = st.columns(5)

# c1.metric(
#     "Average ROE",
#     f"{avg_roe:.2f}%"
# )

# c2.metric(
#     "Median D/E",
#     f"{median_de:.2f}"
# )

# c3.metric(
#     "Companies",
#     total_companies
# )

# c4.metric(
#     "Revenue CAGR",
#     f"{median_growth:.2f}%"
# )

# c5.metric(
#     "Debt Free",
#     debt_free
# )

# st.divider()

# # --------------------------------------------------
# # Two Column Layout
# # --------------------------------------------------

# left, right = st.columns([1, 1])

# # ==================================================
# # LEFT : Sector Donut
# # ==================================================

# with left:

#     st.subheader("Sector Distribution")

#     sector_counts = (
#         sectors["broad_sector"]
#         .value_counts()
#         .reset_index()
#     )

#     sector_counts.columns = [
#         "Sector",
#         "Companies"
#     ]

#     fig = px.pie(
#         sector_counts,
#         names="Sector",
#         values="Companies",
#         hole=0.55
#     )

#     st.plotly_chart(
#         fig,
#         use_container_width=True
#     )

# # ==================================================
# # RIGHT : Top Companies
# # ==================================================

# with right:

#     st.subheader("Top Quality Companies")

#     top = (
#         ratios.sort_values(
#             "composite_quality_score",
#             ascending=False
#         )
#         [
#             [
#                 "company_id",
#                 "composite_quality_score",
#                 "return_on_equity_pct",
#                 "debt_to_equity"
#             ]
#         ]
#         .head(5)
#     )

#     st.dataframe(
#         top,
#         use_container_width=True
#     )

# st.divider()

# # --------------------------------------------------
# # Dataset Preview
# # --------------------------------------------------

# st.subheader("Financial Ratios Preview")

# st.dataframe(
#     ratios.head(20),
#     use_container_width=True
# )