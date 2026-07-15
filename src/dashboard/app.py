"""
Sprint 4 - Day 22
Main Streamlit Dashboard
"""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT))

import streamlit as st

from utils.db import get_all_ratios

st.set_page_config(
    page_title="Nifty 100 Analytics",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📈 Nifty 100 Analytics Dashboard")

# df = get_all_ratios()

# st.write(df.head())

st.markdown("""
Welcome to the Nifty 100 Analytics Dashboard.

Use the sidebar to navigate between dashboard pages.
""")

st.success("Dashboard loaded successfully.")