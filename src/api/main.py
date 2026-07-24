from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from time import time
import sqlite3
from pathlib import Path
from src.api.database import get_connection
from src.api.config import API_VERSION, START_TIME
from src.api.routers import (
    companies,
    screener,
    sectors,
    peers,
    valuation,
    portfolio,
    documents,
    health,
)

# --------------------------------------------------
# Configuration
# --------------------------------------------------

API_VERSION = "1.0.0"

# PROJECT_ROOT = Path(__file__).resolve().parents[2]
# DB_FILE = PROJECT_ROOT / "db" / "nifty100.db"

# START_TIME = time()

# --------------------------------------------------
# FastAPI App
# --------------------------------------------------

app = FastAPI(
    title="Nifty100 Analytics API",
    version=API_VERSION,
    description="REST API for Nifty100 Financial Analytics"
)

# --------------------------------------------------
# Database Connection
# --------------------------------------------------

# def get_connection():
#     """
#     Returns a SQLite database connection.
#     """
#     conn = sqlite3.connect(DB_FILE)
#     conn.row_factory = sqlite3.Row
#     return conn

# --------------------------------------------------
# CORS Middleware
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # Internal use only
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------------------------------
# Request Logging Middleware
# --------------------------------------------------

@app.middleware("http")
async def log_requests(request: Request, call_next):

    start = time()

    response = await call_next(request)

    elapsed = (time() - start) * 1000

    print(
        f"{request.method} "
        f"{request.url.path} "
        f"{elapsed:.2f} ms"
    )

    return response

# --------------------------------------------------
# Routers
# --------------------------------------------------

app.include_router(health.router, prefix="/api/v1", tags=["Health"])
app.include_router(companies.router, prefix="/api/v1", tags=["Companies"])
app.include_router(screener.router, prefix="/api/v1", tags=["Screener"])
app.include_router(sectors.router, prefix="/api/v1", tags=["Sectors"])
app.include_router(peers.router, prefix="/api/v1", tags=["Peers"])
app.include_router(valuation.router, prefix="/api/v1", tags=["Valuation"])
app.include_router(portfolio.router, prefix="/api/v1", tags=["Portfolio"])
app.include_router(documents.router, prefix="/api/v1", tags=["Documents"])