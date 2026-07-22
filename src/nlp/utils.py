"""
Utility functions for NLP Rule Engine
"""

import re


def extract_year(year):
    """
    Extract numeric year from strings like:
    'Mar 2024', 'Dec 2023', '2022'
    """
    if year is None:
        return -1

    match = re.search(r"\d{4}", str(year))
    return int(match.group()) if match else -1


def latest_snapshot(df):
    """
    Return latest record for every company.
    Ignore TTM rows.
    """

    data = df[df["year"] != "TTM"].copy()

    data["sort_year"] = data["year"].apply(extract_year)

    latest = (
        data.sort_values("sort_year")
            .groupby("company_id")
            .tail(1)
            .drop(columns="sort_year")
    )

    return latest


def company_history(df, company_id):
    """
    Return historical records for one company.
    """

    history = df[
        (df["company_id"] == company_id) &
        (df["year"] != "TTM")
    ].copy()

    history["sort_year"] = history["year"].apply(extract_year)

    return history.sort_values("sort_year")