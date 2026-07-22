import sqlite3
import pandas as pd

conn = sqlite3.connect("nifty100.db")

df = pd.read_sql("""
SELECT *
FROM financial_ratios
LIMIT 1
""", conn)

conn.close()

print(df.columns.tolist())