import pandas as pd

df = pd.read_excel(
    "data/raw/stock_prices.xlsx",
    header=None
)

print(df.head())
print(df.shape)