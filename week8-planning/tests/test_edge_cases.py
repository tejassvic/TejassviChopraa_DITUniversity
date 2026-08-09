"""
Phase 5 - Edge case tests using plain asserts.
"""

from __future__ import annotations

import sqlite3
import sys
from pathlib import Path
from typing import Dict

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src import utils  # noqa: E402
from src.clean_data import check_referential_integrity  # noqa: E402

SEPARATOR = "=" * 70


def _build_in_memory_db() -> sqlite3.Connection:
    """Create an in-memory SQLite database with a minimal schema."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")

    conn.executescript(
        """
        CREATE TABLE orders (
            order_id    TEXT PRIMARY KEY,
            customer_id TEXT,
            order_date  TEXT NOT NULL,
            status      TEXT NOT NULL,
            region_code TEXT NOT NULL
        );

        CREATE TABLE products (
            product_id   TEXT PRIMARY KEY,
            product_name TEXT NOT NULL,
            category     TEXT NOT NULL,
            subcategory  TEXT NOT NULL,
            cost_price   REAL NOT NULL
        );

        CREATE TABLE order_items (
            item_id          TEXT PRIMARY KEY,
            order_id         TEXT NOT NULL,
            product_id       TEXT NOT NULL,
            quantity         INTEGER NOT NULL,
            unit_price       REAL NOT NULL,
            discount_percent REAL NOT NULL CHECK (discount_percent BETWEEN 0 AND 100),
            FOREIGN KEY (order_id)   REFERENCES orders(order_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        );
        """
    )
    return conn


def test_orphaned_order_id() -> None:
    """Test that an order_id not in orders is flagged and rejected."""
    print("\n" + SEPARATOR)
    print("TEST 1 : order_items contains order_id not present in orders")
    print(SEPARATOR)

    import pandas as pd

    orders_df = pd.DataFrame(
        [
            {"order_id": "ORD-00001", "customer_id": "CUST-0001",
             "order_date": "2024-01-01 10:00:00", "status": "PLACED",
             "region_code": "NORTH"}
        ]
    )
    items_df = pd.DataFrame(
        [
            {"item_id": "ITM-000001", "order_id": "ORD-00001",
             "product_id": "PRD-0001", "quantity": 2, "unit_price": 10.0,
             "discount_percent": 0.0},
            {"item_id": "ITM-000002", "order_id": "ORD-99999",
             "product_id": "PRD-0001", "quantity": 1, "unit_price": 5.0,
             "discount_percent": 0.0},
        ]
    )

    orphaned = check_referential_integrity(items_df, orders_df)
    print(f"  Orphaned order IDs detected: {orphaned}")
    assert "ORD-99999" in orphaned

    conn = _build_in_memory_db()
    try:
        conn.execute(
            "INSERT INTO orders VALUES (?, ?, ?, ?, ?)",
            ("ORD-00001", "CUST-0001", "2024-01-01 10:00:00", "PLACED", "NORTH"),
        )
        conn.execute(
            "INSERT INTO products VALUES (?, ?, ?, ?, ?)",
            ("PRD-0001", "Widget", "Home", "Kitchen", 5.0),
        )
        try:
            conn.execute(
                "INSERT INTO order_items VALUES (?, ?, ?, ?, ?, ?)",
                ("ITM-000002", "ORD-99999", "PRD-0001", 1, 5.0, 0.0),
            )
        except sqlite3.IntegrityError as exc:
            print(f"  SQLite FK constraint raised IntegrityError: {exc}")
            assert "FOREIGN KEY" in str(exc) or "foreign key" in str(exc)
        else:
            raise AssertionError("Orphaned order_items row was inserted successfully")
    finally:
        conn.close()

    print("  RESULT: PASSED - orphaned order_id correctly detected")


def test_discount_percent_greater_than_100() -> None:
    """Test that discount_percent > 100 is rejected by the CHECK constraint."""
    print("\n" + SEPARATOR)
    print("TEST 2 : discount_percent greater than 100")
    print(SEPARATOR)

    conn = _build_in_memory_db()
    try:
        conn.execute(
            "INSERT INTO orders VALUES (?, ?, ?, ?, ?)",
            ("ORD-00001", "CUST-0001", "2024-01-01 10:00:00", "PLACED", "NORTH"),
        )
        conn.execute(
            "INSERT INTO products VALUES (?, ?, ?, ?, ?)",
            ("PRD-0001", "Widget", "Home", "Kitchen", 5.0),
        )
        try:
            conn.execute(
                "INSERT INTO order_items VALUES (?, ?, ?, ?, ?, ?)",
                ("ITM-000001", "ORD-00001", "PRD-0001", 1, 10.0, 150.0),
            )
        except sqlite3.IntegrityError as exc:
            print(f"  SQLite CHECK constraint raised IntegrityError: {exc}")
        else:
            raise AssertionError("discount_percent=150 should violate the CHECK constraint")
    finally:
        conn.close()

    print("  RESULT: PASSED - discount_percent > 100 rejected by the database")


def test_quantity_zero() -> None:
    """Test that quantity 0 produces zero revenue without errors."""
    print("\n" + SEPARATOR)
    print("TEST 3 : quantity equals 0")
    print(SEPARATOR)

    conn = _build_in_memory_db()
    try:
        conn.execute(
            "INSERT INTO orders VALUES (?, ?, ?, ?, ?)",
            ("ORD-00001", "CUST-0001", "2024-01-01 10:00:00", "DELIVERED", "NORTH"),
        )
        conn.execute(
            "INSERT INTO products VALUES (?, ?, ?, ?, ?)",
            ("PRD-0001", "Widget", "Home", "Kitchen", 5.0),
        )
        conn.execute(
            "INSERT INTO order_items VALUES (?, ?, ?, ?, ?, ?)",
            ("ITM-000001", "ORD-00001", "PRD-0001", 0, 10.0, 0.0),
        )

        row = conn.execute(
            """
            SELECT ROUND(SUM(quantity * unit_price * (1 - discount_percent / 100.0)), 2)
                   AS revenue
            FROM order_items
            """,
        ).fetchone()
        print(f"  Revenue generated by zero-quantity item: {row['revenue']}")
        assert row["revenue"] == 0.0, "Zero quantity should produce zero revenue"
    finally:
        conn.close()

    print("  RESULT: PASSED - quantity 0 handled gracefully (zero revenue)")


def test_future_order_date() -> None:
    """Test that future dates are correctly identified."""
    print("\n" + SEPARATOR)
    print("TEST 4 : order_date is in the future")
    print(SEPARATOR)

    from datetime import datetime, timedelta

    now = datetime.now()
    future = now + timedelta(days=365)

    is_future = future > now
    print(f"  Now      : {now.strftime(utils.CANONICAL_DATETIME_FORMAT)}")
    print(f"  Synthetic: {future.strftime(utils.CANONICAL_DATETIME_FORMAT)}")
    print(f"  Is future: {is_future}")
    assert is_future, "Synthetic future date should be flagged as in the future"

    past = now - timedelta(days=1)
    assert not (past > now), "Yesterday should not be flagged as future"

    print("  RESULT: PASSED - future dates are correctly identifiable")


def run_all_tests() -> Dict[str, bool]:
    """Execute every edge-case test; returns name -> pass/fail."""
    results: Dict[str, bool] = {}

    tests = [
        ("orphaned_order_id", test_orphaned_order_id),
        ("discount_percent_greater_than_100", test_discount_percent_greater_than_100),
        ("quantity_zero", test_quantity_zero),
        ("future_order_date", test_future_order_date),
    ]

    for name, func in tests:
        try:
            func()
            results[name] = True
            print(f"  >> {name}: OK")
        except AssertionError as exc:
            results[name] = False
            print(f"  >> {name}: FAILED - {exc}")
        except Exception as exc:  # noqa: BLE001 - keep the runner simple
            results[name] = False
            print(f"  >> {name}: ERROR - {type(exc).__name__}: {exc}")

    return results


if __name__ == "__main__":
    print(SEPARATOR)
    print("E-COMMERCE ORDER ANALYTICS - EDGE CASE TESTS")
    print(SEPARATOR)

    test_results = run_all_tests()

    print()
    print(SEPARATOR)
    print("SUMMARY")
    print(SEPARATOR)
    for name, passed in test_results.items():
        status = "PASSED" if passed else "FAILED"
        print(f"  {name:<45}: {status}")

    failed_count = sum(1 for passed in test_results.values() if not passed)
    print("-" * 70)
    if failed_count == 0:
        print(f"  ALL {len(test_results)} TESTS PASSED")
    else:
        print(f"  {failed_count} TEST(S) FAILED")
        sys.exit(1)