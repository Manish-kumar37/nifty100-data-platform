from fastapi import APIRouter
from time import time

from src.api.database import get_connection
from src.api.config import API_VERSION, START_TIME

router = APIRouter()

TABLES = [
    "companies",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "analysis",
    "documents",
    "prosandcons",
    "sectors",
    "peer_groups",
    "stock_prices",
    "financial_ratios",
    "peer_percentiles",
]


@router.get("/health")
def health():

    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Get all table names dynamically
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )

        tables = [row[0] for row in cursor.fetchall()]

        row_counts = {}

        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            row_counts[table] = cursor.fetchone()[0]

    finally:
        conn.close()

    return {
        "status": "ok",
        "version": API_VERSION,
        "uptime_seconds": round(time() - START_TIME, 2),
        "db_row_counts": row_counts,
    }