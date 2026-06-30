from src.analytics.cashflow_kpis import *


def test_fcf():

    assert calculate_free_cash_flow(
        100,
        -30
    ) == 70


def test_quality_high():

    assert calculate_cfo_quality(
        120,
        100
    ) == "High Quality"


def test_quality_moderate():

    assert calculate_cfo_quality(
        70,
        100
    ) == "Moderate"


def test_quality_low():

    assert calculate_cfo_quality(
        20,
        100
    ) == "Accrual Risk"


def test_pat_zero():

    assert calculate_cfo_quality(
        20,
        0
    ) is None


def test_asset_light():

    assert calculate_capex_intensity(
        -2,
        100
    ) == "Asset Light"


def test_capital_intensive():

    assert calculate_capex_intensity(
        -20,
        100
    ) == "Capital Intensive"


def test_fcf_conversion():

    assert calculate_fcf_conversion(
        60,
        100
    ) == 60


def test_shareholder_returns():

    assert capital_allocation_pattern(
        100,
        -50,
        -30,
        "High Quality"
    ) == "Shareholder Returns"


def test_growth_by_debt():

    assert capital_allocation_pattern(
        -50,
        -30,
        100
    ) == "Growth Funded by Debt"