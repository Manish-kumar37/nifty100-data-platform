from src.analytics.ratios import *

def test_net_profit_margin():

    assert calculate_net_profit_margin(
        20,
        100
    ) == 20.0


def test_net_profit_margin_zero_sales():

    assert calculate_net_profit_margin(
        20,
        0
    ) is None


def test_operating_profit_margin():

    assert calculate_operating_profit_margin(
        30,
        100
    ) == 30.0


def test_roe():

    assert calculate_roe(
        25,
        50,
        50
    ) == 25.0


def test_negative_equity():

    assert calculate_roe(
        25,
        -50,
        20
    ) is None


def test_roce():

    assert calculate_roce(
        20,
        40,
        40,
        20
    ) == 20.0


def test_roa():

    assert calculate_roa(
        15,
        100
    ) == 15.0


def test_opm_difference():

    assert check_opm_difference(
        20,
        18
    ) is True

def test_debt_free_de():

    assert calculate_debt_to_equity(
        0,
        100,
        50
    ) == 0


def test_high_de():

    assert high_leverage_flag(
        6,
        "Industrials"
    ) is True


def test_bank_de():

    assert high_leverage_flag(
        8,
        "Financials"
    ) is False


def test_icr():

    assert calculate_interest_coverage(
        100,
        20,
        10
    ) == 12.0


def test_icr_zero_interest():

    assert calculate_interest_coverage(
        100,
        20,
        0
    ) is None


def test_debt_free_label():

    assert interest_coverage_label(
        0
    ) == "Debt Free"


def test_icr_warning():

    assert interest_coverage_warning(
        1.2
    ) is True


def test_asset_turnover():

    assert calculate_asset_turnover(
        500,
        250
    ) == 2.0