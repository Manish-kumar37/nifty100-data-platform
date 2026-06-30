"""
Cash Flow KPI Engine
Sprint 2 - Day 11
"""

from typing import Optional


def calculate_free_cash_flow(
    operating_activity: float,
    investing_activity: float
) -> float:
    """
    Free Cash Flow = CFO + CFI
    """

    return operating_activity + investing_activity


def calculate_cfo_quality(
    cfo: float,
    pat: float
):
    """
    CFO / PAT
    """

    if pat == 0:
        return None

    score = cfo / pat

    if score > 1:
        return "High Quality"

    if score >= 0.5:
        return "Moderate"

    return "Accrual Risk"


def calculate_capex_intensity(
    investing_activity: float,
    sales: float
):
    """
    CapEx Intensity (%)
    """

    if sales == 0:
        return None

    intensity = abs(investing_activity) / sales * 100

    if intensity < 3:
        return "Asset Light"

    if intensity <= 8:
        return "Moderate"

    return "Capital Intensive"


def calculate_fcf_conversion(
    free_cash_flow: float,
    operating_profit: float
):
    """
    FCF Conversion (%)
    """

    if operating_profit == 0:
        return None

    return round(
        free_cash_flow / operating_profit * 100,
        2
    )


def capital_allocation_pattern(
    cfo: float,
    cfi: float,
    cff: float,
    cfo_quality: str = None
):
    """
    Capital Allocation Pattern
    """

    signs = (
        cfo > 0,
        cfi > 0,
        cff > 0
    )

    if signs == (True, False, False):
        if cfo_quality == "High Quality":
            return "Shareholder Returns"
        return "Reinvestor"

    if signs == (True, True, False):
        return "Liquidating Assets"

    if signs == (False, True, True):
        return "Distress Signal"

    if signs == (False, False, True):
        return "Growth Funded by Debt"

    if signs == (True, True, True):
        return "Cash Accumulator"

    if signs == (False, False, False):
        return "Pre-Revenue"

    if signs == (True, False, True):
        return "Mixed"

    return "Unknown"