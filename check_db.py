# # check_db.py

# import sqlite3

# conn = sqlite3.connect("nifty100.db")

# cursor = conn.cursor()

# tables = [
#     "companies",
#     "profitandloss",
#     "balancesheet",
#     "cashflow",
#     "analysis",
#     "documents",
#     "prosandcons",
#     "sectors",
#     "peer_groups",
#     "financial_ratios",
#     "stock_prices"
# ]

# for table in tables:

#     count = cursor.execute(
#         f"SELECT COUNT(*) FROM {table}"
#     ).fetchone()[0]

#     print(f"{table}: {count}")

# print("\nFK CHECK")

# fk = cursor.execute(
#     "PRAGMA foreign_key_check;"
# ).fetchall()

# print(fk)

# conn.close()


import sqlite3

conn = sqlite3.connect("nifty100.db")
cursor = conn.cursor()

tables = [
    "companies",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "analysis",
    "documents",
    "prosandcons",
    "sectors",
    "peer_groups",
    "financial_ratios",
    "stock_prices"
]

print("=" * 60)
print("TABLE ROW COUNTS")
print("=" * 60)

for table in tables:

    count = cursor.execute(
        f"SELECT COUNT(*) FROM {table}"
    ).fetchone()[0]

    print(f"{table}: {count}")

print("\n" + "=" * 60)
print("FOREIGN KEY CHECK")
print("=" * 60)

fk = cursor.execute(
    "PRAGMA foreign_key_check;"
).fetchall()

print(fk)

print("\n" + "=" * 60)
print("FINANCIAL RATIOS COLUMNS")
print("=" * 60)

cursor.execute(
    "PRAGMA table_info(financial_ratios)"
)

for column in cursor.fetchall():
    print(column[1])

print("\n" + "=" * 60)
print("SAMPLE KPI DATA")
print("=" * 60)

cursor.execute("""
SELECT
    company_id,
    year,
    net_profit_margin_pct,
    return_on_equity_pct,
    debt_to_equity,
    interest_coverage,
    free_cash_flow_cr,
    revenue_cagr_5yr,
    pat_cagr_5yr,
    eps_cagr_5yr
FROM financial_ratios
LIMIT 10;
""")

for row in cursor.fetchall():
    print(row)

conn.close()