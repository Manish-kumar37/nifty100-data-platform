import pandas as pd

df = pd.read_excel(
    "data/raw/peer_groups.xlsx",
    header=None
)

print(df.head())
print(df.shape)