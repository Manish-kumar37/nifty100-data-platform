from src.etl.loader import load_excel

files = [
    "analysis.xlsx",
    "documents.xlsx",
    "prosandcons.xlsx",
    "sectors.xlsx",
    "peer_groups.xlsx",
    "financial_ratios.xlsx",
    "stock_prices.xlsx"
]

for file in files:

    print("\n" + "=" * 60)
    print(file)
    print("=" * 60)

    df = load_excel(
        file,
        header_row=1
    )

    print(df.head())

    print("\nColumns:")
    print(df.columns.tolist())

    print("\nShape:")
    print(df.shape)