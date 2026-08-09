"""
Phase 3 - Create the SQLite database, schema, and load cleaned data.
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path
from typing import Dict, List

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src import utils  # noqa: E402

SEPARATOR = "=" * 70

TABLE_TO_CSV: Dict[str, str] = {
    "customers": utils.CUSTOMERS_CSV,
    "products": utils.PRODUCTS_CSV,
    "orders": utils.ORDERS_CSV,
    "order_items": utils.ORDER_ITEMS_CSV,
}


def create_database(conn: sqlite3.Connection) -> None:
    """Drop existing tables and re-create the schema from schema.sql."""
    conn.executescript(
        """
        DROP TABLE IF EXISTS order_items;
        DROP TABLE IF EXISTS orders;
        DROP TABLE IF EXISTS products;
        DROP TABLE IF EXISTS customers;
        """
    )

    schema_path = utils.sql_file("schema.sql")
    utils.execute_sql_script(conn, schema_path)
    print(f"  [OK] Schema created from {schema_path}")


def load_csv_into_table(
    conn: sqlite3.Connection,
    table_name: str,
    csv_path: Path,
    columns: List[str],
) -> int:
    """Load a cleaned CSV file into the given table; return rows inserted."""
    df = pd.read_csv(csv_path, dtype=str)

    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise ValueError(f"CSV {csv_path.name} is missing columns: {missing}")

    df = df[columns]

    placeholders = ", ".join(["?"] * len(columns))
    insert_sql = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"

    rows = [tuple(row) for row in df.itertuples(index=False, name=None)]
    conn.executemany(insert_sql, rows)
    return len(rows)


def main() -> None:
    """Entry point: build the database and load all cleaned files."""
    print(SEPARATOR)
    print("PHASE 3 - LOADING CLEANED DATA INTO SQLITE")
    print(SEPARATOR)

    # Ensure the cleaned files exist.
    missing = [csv for csv in TABLE_TO_CSV.values() if not utils.cleaned_csv(csv).exists()]
    if missing:
        print(f"ERROR: cleaned files missing: {missing}")
        print("Run src/clean_data.py first.")
        sys.exit(1)

    # Remove a stale database.
    if utils.DB_PATH.exists():
        utils.DB_PATH.unlink()
        print(f"  [OK] Removed previous database {utils.DB_PATH}")

    conn = utils.get_connection(utils.DB_PATH)
    try:
        create_database(conn)

        column_map = {
            "customers": ["customer_id", "customer_name", "email",
                          "registration_date", "customer_type"],
            "products": ["product_id", "product_name", "category",
                         "subcategory", "cost_price"],
            "orders": ["order_id", "customer_id", "order_date",
                       "status", "region_code"],
            "order_items": ["item_id", "order_id", "product_id",
                            "quantity", "unit_price", "discount_percent"],
        }

        total_rows = 0
        for table, csv_name in TABLE_TO_CSV.items():
            path = utils.cleaned_csv(csv_name)
            inserted = load_csv_into_table(conn, table, path, column_map[table])
            total_rows += inserted
            print(f"  [OK] Loaded {inserted:>6} rows into {table}")

        conn.commit()

        # Sanity checks.
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [r["name"] for r in cursor.fetchall()]
        print(f"  [OK] Tables in database: {', '.join(tables)}")

        cursor = conn.execute(
            "SELECT (SELECT COUNT(*) FROM orders), "
            "(SELECT COUNT(*) FROM order_items), "
            "(SELECT COUNT(*) FROM products), "
            "(SELECT COUNT(*) FROM customers)"
        )
        counts = cursor.fetchone()
        print(
            f"  [OK] Row counts -> orders: {counts[0]}, order_items: {counts[1]}, "
            f"products: {counts[2]}, customers: {counts[3]}"
        )

        cursor = conn.execute(
            """
            SELECT COUNT(*) FROM order_items oi
            LEFT JOIN orders o ON oi.order_id = o.order_id
            WHERE o.order_id IS NULL
            """
        )
        orphaned = cursor.fetchone()[0]
        status = "PASSED" if orphaned == 0 else "FAILED"
        print(f"  [OK] Referential integrity check (items->orders): {status} ({orphaned} orphaned)")

    finally:
        conn.close()

    print(SEPARATOR)
    print(f"Database ready at {utils.DB_PATH}")
    print(SEPARATOR)


if __name__ == "__main__":
    main()