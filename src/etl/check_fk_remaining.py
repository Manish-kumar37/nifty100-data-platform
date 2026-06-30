from src.etl.loader import (
    load_companies,
    load_analysis,
    load_documents,
    load_prosandcons,
    load_sectors,
    load_peer_groups,
    load_financial_ratios,
    load_stock_prices
)

companies = load_companies()

valid_ids = set(companies["id"])

tables = {
    "analysis": load_analysis(),
    "documents": load_documents(),
    "prosandcons": load_prosandcons(),
    "sectors": load_sectors(),
    "peer_groups": load_peer_groups(),
    "financial_ratios": load_financial_ratios(),
    "stock_prices": load_stock_prices()
}

for table_name, df in tables.items():

    invalid = df[
        ~df["company_id"].isin(valid_ids)
    ]

    print(
        f"{table_name}: {len(invalid)} FK violations"
    )

    if len(invalid) > 0:
        print(
            invalid["company_id"]
            .drop_duplicates()
            .tolist()
        )
        print()