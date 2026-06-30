# src/etl/normaliser.py

import pandas as pd


def normalize_ticker(ticker):
    """
    Convert ticker to uppercase and remove extra spaces.

    Examples:
    ' tcs ' -> 'TCS'
    'infy' -> 'INFY'
    """

    if pd.isna(ticker):
        return None

    return str(ticker).strip().upper()


def normalize_year(year):
    """
    Convert year labels like:
    Mar-24 -> 2024-03
    Mar-23 -> 2023-03
    Dec-22 -> 2022-12
    """

    if pd.isna(year):
        return None

    year = str(year).strip()

    months = {
        "Jan": "01",
        "Feb": "02",
        "Mar": "03",
        "Apr": "04",
        "May": "05",
        "Jun": "06",
        "Jul": "07",
        "Aug": "08",
        "Sep": "09",
        "Oct": "10",
        "Nov": "11",
        "Dec": "12",
    }

    if "-" in year:
        month, yy = year.split("-")

        month_num = months.get(month)

        if month_num:
            return f"20{yy}-{month_num}"

    return year