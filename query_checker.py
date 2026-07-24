import sqlite3
from pathlib import Path

db = Path("nifty100.db")

conn = sqlite3.connect(db)

print(conn.execute(
    "SELECT name FROM sqlite_master WHERE type='table';"
).fetchall())

conn.close()