from src.etl.loader import (
    load_analysis,
    load_documents,
    load_prosandcons,
    load_sectors,
    load_peer_groups,
    load_financial_ratios,
    load_stock_prices
)

tables = {
    "analysis": load_analysis(),
    "documents": load_documents(),
    "prosandcons": load_prosandcons(),
    "sectors": load_sectors(),
    "peer_groups": load_peer_groups(),
    "financial_ratios": load_financial_ratios(),
    "stock_prices": load_stock_prices()
}

for name, df in tables.items():

    print("\n" + "=" * 50)
    print(name)
    print("=" * 50)

    print(df.columns.tolist())