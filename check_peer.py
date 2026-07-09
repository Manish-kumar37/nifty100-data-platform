import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

df = pd.read_sql(
    "SELECT * FROM peer_groups",
    conn
)

conn.close()

print(df.columns.tolist())
print()
print(df.head(20))
print()
print("Rows:", len(df))