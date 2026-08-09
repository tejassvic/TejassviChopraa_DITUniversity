"""
Shared helper utilities for the E-Commerce Order Analytics System.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Optional

# Project paths
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent
RAW_DATA_DIR: Path = PROJECT_ROOT / "data" / "raw"
CLEANED_DATA_DIR: Path = PROJECT_ROOT / "data" / "cleaned"
SQL_DIR: Path = PROJECT_ROOT / "sql"
REPORTS_DIR: Path = PROJECT_ROOT / "reports"
DB_PATH: Path = PROJECT_ROOT / "ecommerce.db"

# CSV file names
ORDERS_CSV = "orders.csv"
ORDER_ITEMS_CSV = "order_items.csv"
PRODUCTS_CSV = "products.csv"
CUSTOMERS_CSV = "customers.csv"


def raw_csv(name: str) -> Path:
    """Return path of a raw CSV file."""
    return RAW_DATA_DIR / name


def cleaned_csv(name: str) -> Path:
    """Return path of a cleaned CSV file."""
    return CLEANED_DATA_DIR / name


def sql_file(name: str) -> Path:
    """Return path of a SQL script."""
    return SQL_DIR / name


def report_file(name: str) -> Path:
    """Return path of a report file."""
    return REPORTS_DIR / name


def get_connection(db_path: Path | str | None = None) -> sqlite3.Connection:
    """Open a SQLite connection with row factory and foreign keys enabled."""
    if db_path is None:
        db_path = DB_PATH

    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def execute_sql_script(
    conn: sqlite3.Connection,
    script: str | Path,
    *,
    fetch_results: bool = False,
) -> Optional[list[sqlite3.Row]]:
    """
    Execute a SQL script (file or inline string) against a connection.

    Returns rows of the final statement when fetch_results=True.
    """
    if isinstance(script, Path):
        script_text = script.read_text(encoding="utf-8")
    else:
        script_text = script

    # Remove line comments before splitting on semicolons, so semicolons
    # inside comments do not break statements.
    cleaned_lines = []
    for line in script_text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("--"):
            continue
        comment_pos = line.find("--")
        if comment_pos != -1:
            line = line[:comment_pos]
        cleaned_lines.append(line)
    cleaned_text = "\n".join(cleaned_lines)

    statements = [stmt.strip() for stmt in cleaned_text.split(";") if stmt.strip()]

    result: Optional[list[sqlite3.Row]] = None
    for statement in statements:
        cursor = conn.execute(statement)
        if fetch_results and statement.lower().startswith(("select", "with", "pragma")):
            result = cursor.fetchall()

    return result


# Date formats
CANONICAL_DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
WRONG_DATETIME_FORMAT = "%d-%m-%Y"
DATE_ONLY_FORMAT = "%Y-%m-%d"

DT_FORMATS_TO_TRY = (
    CANONICAL_DATETIME_FORMAT,
    WRONG_DATETIME_FORMAT,
    DATE_ONLY_FORMAT,
)


def parse_datetime_loose(value: str) -> Optional[datetime]:
    """Try to parse a date-time string using known formats; return None if unparseable."""
    if value is None:
        return None

    text = str(value).strip()
    if not text:
        return None

    text = text.replace(" UTC", "").strip()

    for fmt in DT_FORMATS_TO_TRY:
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue

    return None


def format_datetime(dt: datetime) -> str:
    """Format a datetime using the canonical project format."""
    return dt.strftime(CANONICAL_DATETIME_FORMAT)


# Ensure directories exist
for directory in (RAW_DATA_DIR, CLEANED_DATA_DIR, REPORTS_DIR):
    directory.mkdir(parents=True, exist_ok=True)