"""
Composite Quality Score
Sprint 2
"""


def quality_score(row):

    score = 0

    # Profitability
    if row["return_on_equity_pct"] is not None:
        if row["return_on_equity_pct"] >= 15:
            score += 2
        elif row["return_on_equity_pct"] >= 10:
            score += 1

    # Leverage
    if row["debt_to_equity"] is not None:
        if row["debt_to_equity"] < 1:
            score += 2
        elif row["debt_to_equity"] < 2:
            score += 1

    # Interest Coverage
    if row["interest_coverage"] is not None:
        if row["interest_coverage"] > 3:
            score += 2
        elif row["interest_coverage"] > 1.5:
            score += 1

    # Cash Flow
    if row["free_cash_flow_cr"] is not None:
        if row["free_cash_flow_cr"] > 0:
            score += 2

    # Asset Turnover
    if row["asset_turnover"] is not None:
        if row["asset_turnover"] > 1:
            score += 2

    return score