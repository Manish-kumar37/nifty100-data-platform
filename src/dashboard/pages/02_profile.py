import streamlit as st

from utils.db import (
    get_companies,
    get_company_ratios
)

st.title("🏢 Company Profile")

companies = get_companies()

company_list = sorted(companies["id"].unique())

selected = st.selectbox(
    "Select Company",
    company_list
)

company_data = get_company_ratios(selected)

st.write(company_data.head())