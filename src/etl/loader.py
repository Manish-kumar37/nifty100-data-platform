# src/etl/loader.py

import pandas as pd
from pathlib import Path

from src.etl.normaliser import (
    normalize_ticker,
    normalize_year
)

DATA_PATH = Path("data/raw")


def load_excel(file_name, header_row):
    """
    Generic Excel loader.
    """

    file_path = DATA_PATH / file_name

    return pd.read_excel(
        file_path,
        header=header_row
    )


def load_companies():
    """
    Load companies.xlsx
    """

    df = load_excel(
        "companies.xlsx",
        header_row=1
    )

    df["id"] = df["id"].apply(
        normalize_ticker
    )
 
    return df


def load_profitandloss():
    """
    Load profitandloss.xlsx
    """

    df = load_excel(
        "profitandloss.xlsx",
        header_row=1
    )

    df["company_id"] = df["company_id"].apply(
        normalize_ticker
    )

    df["year"] = df["year"].apply(
        normalize_year
    )

    duplicate_count = df.duplicated(
        subset=["company_id", "year"]
    ).sum()

    print(f"P&L duplicates: {duplicate_count}")

    df = df.drop_duplicates(
        subset=["company_id", "year"],
        keep="first"
    )

    return df


def load_balancesheet():
    """
    Load balancesheet.xlsx
    """

    df = load_excel(
        "balancesheet.xlsx",
        header_row=1
    )

    df["company_id"] = df["company_id"].apply(
        normalize_ticker
    )

    df["year"] = df["year"].apply(
        normalize_year
    )

    duplicate_count = df.duplicated(
        subset=["company_id", "year"]
    ).sum()

    print(f"BS duplicates: {duplicate_count}")

    df = df.drop_duplicates(
        subset=["company_id", "year"],
        keep="first"
    )

    return df


def load_cashflow():
    """
    Load cashflow.xlsx
    """

    df = load_excel(
        "cashflow.xlsx",
        header_row=1
    )

    df["company_id"] = df["company_id"].apply(
        normalize_ticker
    )

    df["year"] = df["year"].apply(
        normalize_year
    )

    duplicate_count = df.duplicated(
        subset=["company_id", "year"]
    ).sum()

    print(f"CF duplicates: {duplicate_count}")

    df = df.drop_duplicates(
        subset=["company_id", "year"],
        keep="first"
    )

    return df


if __name__ == "__main__":

    companies = load_companies()
    pnl = load_profitandloss()
    bs = load_balancesheet()
    cf = load_cashflow()

    print(f"Companies: {len(companies)}")
    print(f"Profit & Loss: {len(pnl)}")
    print(f"Balance Sheet: {len(bs)}")
    print(f"Cash Flow: {len(cf)}")

def load_analysis():

    df = load_excel(
        "analysis.xlsx",
        header_row=1
    )

    df["company_id"] = df["company_id"].apply(
        normalize_ticker
    )

    return df    

def load_documents():

    df = load_excel(
        "documents.xlsx",
        header_row=1
    )

    df["company_id"] = df["company_id"].apply(
        normalize_ticker
    )

    return df

def load_prosandcons():

    df = load_excel(
        "prosandcons.xlsx",
        header_row=1
    )

    df["company_id"] = df["company_id"].apply(
        normalize_ticker
    )

    return df

def load_sectors():

    df = pd.read_excel(
        DATA_PATH / "sectors.xlsx",
        header=0
    )

    df["company_id"] = df["company_id"].apply(
        normalize_ticker
    )

    return df    

def load_peer_groups():

    df = pd.read_excel(
        DATA_PATH / "peer_groups.xlsx",
        header=0
    )

    df["company_id"] = df["company_id"].apply(
        normalize_ticker
    )

    return df

def load_financial_ratios():

    df = pd.read_excel(
        DATA_PATH / "financial_ratios.xlsx",
        header=0
    )

    df["company_id"] = df["company_id"].apply(
        normalize_ticker
    )

    df["year"] = df["year"].apply(
        normalize_year
    )

    return df

def load_stock_prices():

    df = pd.read_excel(
        DATA_PATH / "stock_prices.xlsx",
        header=0
    )

    df["company_id"] = df["company_id"].apply(
        normalize_ticker
    )

    return df