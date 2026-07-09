"""
Sprint 3 - Day 16
Preset Screeners
"""

from src.screener.engine import (
    load_financial_ratios,
    load_config,
    apply_filters
)

CONFIG_PATH = "config/screener_config.yaml"


def _run_preset(preset_name):
    """
    Run a screener preset.
    """

    df = load_financial_ratios()

    config = load_config(CONFIG_PATH)

    return apply_filters(
        df,
        config[preset_name]
    )


def quality_compounder():
    return _run_preset("quality_compounder")


def value_pick():
    return _run_preset("value_pick")


def growth_accelerator():
    return _run_preset("growth_accelerator")


def dividend_champion():
    return _run_preset("dividend_champion")


def debt_free_blue_chip():
    return _run_preset("debt_free_blue_chip")


def turnaround_watch():
    return _run_preset("turnaround_watch")


if __name__ == "__main__":

    result = quality_compounder()

    print()

    print("Companies Found:", len(result))

    print()

    print(
        result[
            [
                "company_id",
                "year",
                "return_on_equity_pct",
                "debt_to_equity",
                "free_cash_flow_cr",
                "revenue_cagr_5yr"
            ]
        ].head(20)
    )

presets = [
    ("Quality Compounder", quality_compounder),
    ("Value Pick", value_pick),
    ("Growth Accelerator", growth_accelerator),
    ("Dividend Champion", dividend_champion),
    ("Debt-Free Blue Chip", debt_free_blue_chip),
    ("Turnaround Watch", turnaround_watch),
]

for name, func in presets:

    result = func()

    print(f"{name}: {len(result)} companies")    

qc = quality_compounder()

print(
    qc[
        [
            "company_id",
            "return_on_equity_pct",
            "debt_to_equity",
            "free_cash_flow_cr",
            "revenue_cagr_5yr"
        ]
    ].head(10)
)    