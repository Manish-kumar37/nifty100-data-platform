"""
Profitability, Leverage and Efficiency Ratio Engine
Sprint 2 - Day 08
"""

from typing import Optional


def calculate_net_profit_margin(
    net_profit: float,
    sales: float
) -> Optional[float]:
    """
    Net Profit Margin (%)

    Formula:
        (Net Profit / Sales) * 100
    """

    if sales == 0:
        return None

    return round(
        (net_profit / sales) * 100,
        2
    )


def calculate_operating_profit_margin(
    operating_profit: float,
    sales: float
) -> Optional[float]:
    """
    Operating Profit Margin (%)
    """

    if sales == 0:
        return None

    return round(
        (operating_profit / sales) * 100,
        2
    )


def check_opm_difference(
    calculated_opm: float,
    source_opm: float
) -> bool:
    """
    Returns True if difference > 1%
    """

    if (
        calculated_opm is None
        or
        source_opm is None
    ):
        return False

    return abs(
        calculated_opm - source_opm
    ) > 1


def calculate_roe(
    net_profit: float,
    equity_capital: float,
    reserves: float
) -> Optional[float]:
    """
    Return on Equity
    """

    equity = (
        equity_capital
        +
        reserves
    )

    if equity <= 0:
        return None

    return round(
        (net_profit / equity) * 100,
        2
    )


def calculate_roce(
    ebit: float,
    equity_capital: float,
    reserves: float,
    borrowings: float
) -> Optional[float]:
    """
    Return on Capital Employed
    """

    capital = (
        equity_capital
        +
        reserves
        +
        borrowings
    )

    if capital <= 0:
        return None

    return round(
        (ebit / capital) * 100,
        2
    )


def calculate_roa(
    net_profit: float,
    total_assets: float
) -> Optional[float]:
    """
    Return on Assets
    """

    if total_assets == 0:
        return None

    return round(
        (net_profit / total_assets) * 100,
        2
    )
def calculate_debt_to_equity(
    borrowings: float,
    equity_capital: float,
    reserves: float
):
    """
    Debt to Equity Ratio
    """

    if borrowings == 0:
        return 0

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return round(borrowings / equity, 2)


def high_leverage_flag(
    debt_to_equity,
    sector
):
    """
    Banks/NBFCs naturally operate
    with high leverage.

    Therefore D/E warning is suppressed.
    """

    if sector == "Financials":
        return False

    if debt_to_equity is None:
        return False

    return debt_to_equity > 5


def calculate_interest_coverage(
    operating_profit: float,
    other_income: float,
    interest: float
):
    """
    Interest Coverage Ratio
    """

    if interest == 0:
        return None

    return round(
        (operating_profit + other_income) / interest,
        2
    )


def interest_coverage_label(
    interest: float
):
    """
    Debt Free label
    """

    if interest == 0:
        return "Debt Free"

    return None


def interest_coverage_warning(
    icr
):
    """
    Company cannot comfortably pay interest.
    """

    if icr is None:
        return False

    return icr < 1.5


def calculate_net_debt(
    borrowings: float,
    investments: float
):
    """
    Net Debt
    """

    return borrowings - investments


def calculate_asset_turnover(
    sales: float,
    total_assets: float
):
    """
    Asset Turnover
    """

    if total_assets == 0:
        return None

    return round(
        sales / total_assets,
        2
    )