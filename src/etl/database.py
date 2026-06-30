import sqlite3
from pathlib import Path
from src.etl.audit import save_load_audit
from src.etl.loader import (
    load_companies,
    load_profitandloss,
    load_balancesheet,
    load_cashflow
)
from src.etl.loader import (
    load_analysis,
    load_documents,
    load_prosandcons,
    load_sectors,
    load_peer_groups,
    load_financial_ratios,
    load_stock_prices
)
from src.etl.validator import filter_valid_companies

PROJECT_ROOT = Path.cwd()
DB_PATH = PROJECT_ROOT / "nifty100.db"


def create_connection():
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def create_database():

    with create_connection() as conn:

        with open(
            PROJECT_ROOT / "db" / "schema.sql",
            "r",
            encoding="utf-8"
        ) as file:

            schema = file.read()

        conn.executescript(schema)

    print("Database created successfully!")


def load_dataframe(df, table_name):

    with create_connection() as conn:

        df.to_sql(
            table_name,
            conn,
            if_exists="append",
            index=False
        )

    print(f"{table_name} loaded: {len(df)} rows")


def load_core_tables():

    audit_rows = []

    # -----------------------------
    # LOAD SOURCE FILES
    # -----------------------------

    companies = load_companies()

    pnl_raw = load_profitandloss()
    bs_raw = load_balancesheet()
    cf_raw = load_cashflow()

    analysis_raw = load_analysis()
    documents_raw = load_documents()
    prosandcons_raw = load_prosandcons()
    sectors_raw = load_sectors()
    peer_groups_raw = load_peer_groups()
    financial_ratios_raw = load_financial_ratios()
    stock_prices_raw = load_stock_prices()

    # -----------------------------
    # FILTER INVALID FK RECORDS
    # -----------------------------

    pnl = filter_valid_companies(
        companies,
        pnl_raw
    )

    bs = filter_valid_companies(
        companies,
        bs_raw
    )

    cf = filter_valid_companies(
        companies,
        cf_raw
    )

    analysis = filter_valid_companies(
        companies,
        analysis_raw
    )

    documents = filter_valid_companies(
        companies,
        documents_raw
    )

    prosandcons = filter_valid_companies(
        companies,
        prosandcons_raw
    )

    sectors = filter_valid_companies(
        companies,
        sectors_raw
    )

    peer_groups = filter_valid_companies(
        companies,
        peer_groups_raw
    )

    financial_ratios = filter_valid_companies(
        companies,
        financial_ratios_raw
    )

    stock_prices = filter_valid_companies(
        companies,
        stock_prices_raw
    )

    # -----------------------------
    # LOAD INTO SQLITE
    # -----------------------------

    load_dataframe(companies, "companies")

    load_dataframe(pnl, "profitandloss")

    load_dataframe(bs, "balancesheet")

    load_dataframe(cf, "cashflow")

    load_dataframe(analysis, "analysis")

    load_dataframe(documents, "documents")

    load_dataframe(prosandcons, "prosandcons")

    load_dataframe(sectors, "sectors")

    load_dataframe(peer_groups, "peer_groups")

    load_dataframe(
        financial_ratios,
        "financial_ratios"
    )

    load_dataframe(
        stock_prices,
        "stock_prices"
    )

    # -----------------------------
    # AUDIT
    # -----------------------------

    tables = [
        ("companies", companies, companies),
        ("profitandloss", pnl_raw, pnl),
        ("balancesheet", bs_raw, bs),
        ("cashflow", cf_raw, cf),
        ("analysis", analysis_raw, analysis),
        ("documents", documents_raw, documents),
        ("prosandcons", prosandcons_raw, prosandcons),
        ("sectors", sectors_raw, sectors),
        ("peer_groups", peer_groups_raw, peer_groups),
        (
            "financial_ratios",
            financial_ratios_raw,
            financial_ratios
        ),
        (
            "stock_prices",
            stock_prices_raw,
            stock_prices
        )
    ]

    for table_name, source_df, loaded_df in tables:

        audit_rows.append({
            "table": table_name,
            "source_rows": len(source_df),
            "loaded_rows": len(loaded_df),
            "rejected_rows":
                len(source_df) - len(loaded_df)
        })

    save_load_audit(audit_rows)

    print("\nCore tables loaded successfully.")
if __name__ == "__main__":

    create_database()
    load_core_tables()

# def load_core_tables():

#     audit_rows = []

#     companies = load_companies()

#     pnl_raw = load_profitandloss()
#     bs_raw = load_balancesheet()
#     cf_raw = load_cashflow()

#     pnl = filter_valid_companies(
#         companies,
#         pnl_raw
#     )

#     bs = filter_valid_companies(
#         companies,
#         bs_raw
#     )

#     cf = filter_valid_companies(
#         companies,
#         cf_raw
#     )

#     load_dataframe(companies, "companies")
#     load_dataframe(pnl, "profitandloss")
#     load_dataframe(bs, "balancesheet")
#     load_dataframe(cf, "cashflow")

#     audit_rows.append({
#         "table": "companies",
#         "source_rows": len(companies),
#         "loaded_rows": len(companies),
#         "rejected_rows": 0
#     })

#     audit_rows.append({
#         "table": "profitandloss",
#         "source_rows": len(pnl_raw),
#         "loaded_rows": len(pnl),
#         "rejected_rows": len(pnl_raw) - len(pnl)
#     })

#     audit_rows.append({
#         "table": "balancesheet",
#         "source_rows": len(bs_raw),
#         "loaded_rows": len(bs),
#         "rejected_rows": len(bs_raw) - len(bs)
#     })

#     audit_rows.append({
#         "table": "cashflow",
#         "source_rows": len(cf_raw),
#         "loaded_rows": len(cf),
#         "rejected_rows": len(cf_raw) - len(cf)
#     })

#     save_load_audit(audit_rows)

#     print("\nCore tables loaded successfully.")    