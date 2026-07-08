import pandas as pd

from src.screener.engine import apply_filters


def sample_df():
    return pd.DataFrame({
        "company_id": ["A", "B", "C"],
        "broad_sector": ["IT", "Financials", "IT"],
        "return_on_equity_pct": [20, 25, 10],
        "debt_to_equity": [0.5, 8.0, 2.5],
        "free_cash_flow_cr": [100, 200, -50],
        "revenue_cagr_5yr": [15, 18, 5],
        "pat_cagr_5yr": [22, 30, 8],
        "operating_profit_margin_pct": [20, 18, 10],
        "interest_coverage": [5, None, 1],
        "asset_turnover": [1.5, 0.8, 0.5],
        "net_profit": [1000, 800, 100],
        "eps_cagr_5yr": [18, 25, 4],
        "sales": [8000, 9000, 2000]
    })


def test_roe_filter():
    df = sample_df()
    result = apply_filters(df, {"roe_min": 15})
    assert len(result) == 2


def test_de_filter_skips_financials():
    df = sample_df()
    result = apply_filters(df, {"debt_to_equity_max": 1})
    assert "B" in result["company_id"].values


def test_fcf_filter():
    df = sample_df()
    result = apply_filters(df, {"free_cash_flow_min": 0})
    assert len(result) == 2


def test_sales_filter():
    df = sample_df()
    result = apply_filters(df, {"sales_min": 5000})
    assert len(result) == 2


def test_opm_filter():
    df = sample_df()
    result = apply_filters(df, {"operating_profit_margin_min": 15})
    assert len(result) == 2


def test_eps_filter():
    df = sample_df()
    result = apply_filters(df, {"eps_cagr_5yr_min": 15})
    assert len(result) == 2