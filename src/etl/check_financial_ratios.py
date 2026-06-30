import pandas as pd

df = pd.read_excel(
    "data/raw/financial_ratios.xlsx",
    header=None
)

print(df.head())
print(df.shape)