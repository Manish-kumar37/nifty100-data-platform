import pandas as pd
def make_rule(rule_type, rule_id, text, confidence):
    return {
        "type": rule_type,
        "rule_id": rule_id,
        "text": text,
        "confidence_pct": confidence,
    }
def rule_pr01(company):

    roe = company.get("roe_percentage")

    if pd.notna(roe) and roe > 20:

        return {
            "type": "pro",
            "rule_id": "PR01",
            "text": "Consistently high return on equity above 20% demonstrates exceptional capital efficiency.",
            "confidence_pct": 95
        }

    return None

def rule_pr02(company):

    if company["free_cash_flow_cr"] > 0:

        return {
            "type": "pro",
            "rule_id": "PR02",
            "text": "Strong free cash flow generation indicates healthy business fundamentals.",
            "confidence_pct": 90
        }

    return None

def rule_pr03(company):

    if company["debt_to_equity"] == 0:

        return {
            "type": "pro",
            "rule_id": "PR03",
            "text": "Debt-free balance sheet provides financial flexibility and eliminates interest burden.",
            "confidence_pct": 95
        }

    return None

def rule_pr04(company):

    if company["revenue_cagr_5yr"] > 15:

        return {
            "type": "pro",
            "rule_id": "PR04",
            "text": "Revenue growing above 15% CAGR over five years reflects strong business momentum.",
            "confidence_pct": 90
        }

    return None

def rule_pr05(company):

    if company["operating_profit_margin_pct"] > 25:

        return {
            "type": "pro",
            "rule_id": "PR05",
            "text": "Operating profit margin above 25% indicates strong pricing power and cost discipline.",
            "confidence_pct": 90
        }

    return None

def rule_pr06(company):

    if company["pat_cagr_5yr"] > 20:

        return {
            "type": "pro",
            "rule_id": "PR06",
            "text": "Net profit compounding above 20% over five years creates significant shareholder value.",
            "confidence_pct": 90
        }

    return None

def rule_pr07(company):

    if (
        company["interest_coverage"] > 10
        or company["debt_to_equity"] == 0
    ):

        return {
            "type": "pro",
            "rule_id": "PR07",
            "text": "Very high interest coverage reflects negligible financial stress from debt servicing.",
            "confidence_pct": 90
        }

    return None

def rule_pr08(company):

    if company["dividend_payout"] > 20:

        return {
            "type": "pro",
            "rule_id": "PR08",
            "text": "Healthy dividend payout reflects management's commitment to shareholder returns.",
            "confidence_pct": 75
        }

    return None    

def rule_pr09(company):

    if company["eps_cagr_5yr"] > 15:

        return {
            "type": "pro",
            "rule_id": "PR09",
            "text": "EPS growing above 15% CAGR indicates strong earnings quality and long-term compounding.",
            "confidence_pct": 90
        }

    return None

def rule_pr10(history):
    """
    ROE improving for 3 consecutive years.
    """

    if len(history) < 3:
        return None

    roe = history["roe_percentage"].tail(3).tolist()

    if roe[0] < roe[1] < roe[2]:

        return make_rule(
            "pro",
            "PR10",
            "Return on equity improving for three consecutive years shows strengthening business quality.",
            90
        )

    return None
def rule_pr11(company):

    if company["pat_cagr_5yr"] > company["revenue_cagr_5yr"]:

        return {
            "type": "pro",
            "rule_id": "PR11",
            "text": "Profit growing faster than revenue indicates improving operating leverage and scale benefits.",
            "confidence_pct": 85
        }

    return None    

def rule_pr12(history):
    """
    Assets increasing while borrowings decline.
    """

    if len(history) < 3:
        return None

    assets = history["total_assets"].tail(3).tolist()

    debt = history["borrowings"].tail(3).tolist()

    if (
        assets[0] < assets[1] < assets[2]
        and
        debt[0] > debt[1] > debt[2]
    ):

        return make_rule(
            "pro",
            "PR12",
            "Growing asset base funded with declining borrowings reflects self-sustaining growth.",
            85
        )

    return None
PRO_RULES = [
    rule_pr01,
    rule_pr02,
    rule_pr03,
    rule_pr04,
    rule_pr05,
    rule_pr06,
    rule_pr07,
    rule_pr08,
    rule_pr09,
    rule_pr10,
    rule_pr11,
    rule_pr12,
]
   

def rule_cr01(company):

    if company["debt_to_equity"] > 2:

        return make_rule(
            "con",
            "CR01",
            f"Debt-to-equity ratio of {company['debt_to_equity']:.2f} is elevated and warrants monitoring.",
            95,
        )

    return None

def rule_cr02(company):

    if company["free_cash_flow_cr"] < 0:

        return make_rule(
            "con",
            "CR02",
            "Negative free cash flow raises concerns about cash generation quality.",
            90,
        )

    return None

def rule_cr03(company):

    if company["operating_profit_margin_pct"] < 10:

        return make_rule(
            "con",
            "CR03",
            "Operating margins are weak and may indicate pricing or cost pressure.",
            85,
        )

    return None

def rule_cr04(company):

    if company["net_profit"] < 0:

        return make_rule(
            "con",
            "CR04",
            "Company reported a net loss in the most recent financial year.",
            95,
        )

    return None

def rule_cr05(company):

    if company["revenue_cagr_5yr"] < 5:

        return make_rule(
            "con",
            "CR05",
            "Revenue growth below 5% over five years indicates limited business momentum.",
            85,
        )

    return None  

def rule_cr06(company):

    if company["interest_coverage"] < 1.5:

        return make_rule(
            "con",
            "CR06",
            "Interest coverage below 1.5x indicates elevated debt servicing risk.",
            95,
        )

    return None  

def rule_cr07(company):

    if company["dividend_payout"] > 100:

        return make_rule(
            "con",
            "CR07",
            "Dividend payout above 100% may be unsustainable.",
            90,
        )

    return None

def rule_cr08(history):
    """
    Debt increasing for 3 years.
    """

    if len(history) < 3:
        return None

    debt = history["debt_to_equity"].tail(3).tolist()

    if debt[0] < debt[1] < debt[2]:

        return make_rule(
            "con",
            "CR08",
            "Debt-to-equity ratio has increased for three consecutive years, indicating rising leverage risk.",
            90
        )

    return None

def rule_cr09(history):
    """
    EPS declining for 3 years.
    """

    if len(history) < 3:
        return None

    eps = history["eps"].tail(3).tolist()

    if eps[0] > eps[1] > eps[2]:

        return make_rule(
            "con",
            "CR09",
            "Earnings per share have declined for three consecutive years, indicating weakening profitability.",
            90
        )

    return None
def rule_cr10(company):

    if company["roce_percentage"] < 10:

        return make_rule(
            "con",
            "CR10",
            "Return on capital employed below 10% suggests weak capital efficiency.",
            90,
        )

    return None

def rule_cr12(company):

    if company["revenue_cagr_10yr"] < 5:

        return make_rule(
            "con",
            "CR12",
            "Long-term revenue growth remains below 5%, indicating limited business expansion.",
            80,
        )

    return None

CON_RULES = [
    rule_cr01,
    rule_cr02,
    rule_cr03,
    rule_cr04,
    rule_cr05,
    rule_cr06,
    rule_cr07,
    rule_cr08,
    rule_cr09,
    rule_cr10,
    rule_cr12,
]
