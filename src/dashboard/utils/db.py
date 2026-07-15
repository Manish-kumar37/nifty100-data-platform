"""
Sprint 4
Dashboard Data Service
"""

import sqlite3
import pandas as pd
import streamlit as st


DB_PATH = "nifty100.db"


# ==========================================================
# Core Query Function
# ==========================================================

@st.cache_data(ttl=600)
def run_query(query, params=None):

    conn = sqlite3.connect(DB_PATH)

    if params is None:
        df = pd.read_sql(query, conn)

    else:
        df = pd.read_sql(
            query,
            conn,
            params=params
        )

    conn.close()

    return df


# ==========================================================
# Basic Tables
# ==========================================================

@st.cache_data(ttl=600)
def get_companies():

    return run_query(
        "SELECT * FROM companies"
    )


@st.cache_data(ttl=600)
def get_all_ratios():

    return run_query(
        "SELECT * FROM financial_ratios"
    )


@st.cache_data(ttl=600)
def get_sectors():

    return run_query(
        "SELECT * FROM sectors"
    )


@st.cache_data(ttl=600)
def get_peer_groups():

    return run_query(
        "SELECT * FROM peer_groups"
    )


# ==========================================================
# Company Functions
# ==========================================================

@st.cache_data(ttl=600)
def get_company_ratios(ticker):

    df = get_all_ratios()

    return df[
        df["company_id"] == ticker
    ].copy()

@st.cache_data(ttl=600)
def get_ratios():

    return run_query(
        "SELECT * FROM financial_ratios"
    )

@st.cache_data(ttl=600)
def get_latest_ratios():

    df = get_ratios()

    # Ignore TTM for dashboard KPIs
    df = df[df["year"] != "TTM"].copy()

    df["sort_year"] = (
        df["year"]
        .str.extract(r"(\d{4})")
        .astype(int)
    )

    df = (
        df.sort_values("sort_year")
          .groupby("company_id")
          .tail(1)
          .drop(columns="sort_year")
    )

    return df


# ==========================================================
# Dashboard Functions
# ==========================================================

@st.cache_data(ttl=600)
def get_dashboard_data(year):

    ratios = get_all_ratios()

    sectors = get_sectors()

    ratios = ratios[
        ratios["year"] == year
    ].copy()

    return {

        "ratios": ratios,

        "companies": get_companies(),

        "sectors": sectors

    }


@st.cache_data(ttl=600)
def get_top_quality(year):

    ratios = get_all_ratios()

    ratios = ratios[
        ratios["year"] == year
    ]

    return (
        ratios
        .sort_values(
            "return_on_equity_pct",
            ascending=False
        )
        .head(5)
    )