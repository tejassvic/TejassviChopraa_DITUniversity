"""
Phase 4 - CLI reporting tool using only the sqlite3 standard library.
"""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src import utils  # noqa: E402

SEPARATOR = "=" * 72

GRANULARITY_DAYS: Dict[str, int] = {
    "daily": 1,
    "weekly": 7,
    "monthly": 30,
}


def parse_user_date(value: str) -> datetime:
    """Parse a user-supplied date (YYYY-MM-DD or YYYY-MM-DD HH:MM:SS)."""
    text = value.strip()
    for fmt in (utils.CANONICAL_DATETIME_FORMAT, "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt)
        except ValueError:
            continue
    raise ValueError(f"Could not parse date '{value}'. Use YYYY-MM-DD.")


def ask_for_dates() -> Tuple[str, str]:
    """Prompt the user for a start and end date for the report."""
    while True:
        start_raw = input("Enter start date (YYYY-MM-DD): ").strip()
        end_raw = input("Enter end date (YYYY-MM-DD): ").strip()
        try:
            start_dt = parse_user_date(start_raw)
            end_dt = parse_user_date(end_raw)
        except ValueError as exc:
            print(f"  [ERROR] {exc}")
            continue

        if start_dt > end_dt:
            print("  [ERROR] Start date must not be after end date.")
            continue

        start_date = start_dt.strftime("%Y-%m-%d")
        end_date = end_dt.strftime("%Y-%m-%d")
        return start_date, end_date


def ask_for_report_type() -> str:
    """Prompt the user for a report granularity (daily / weekly / monthly)."""
    while True:
        value = input("Report type (daily / weekly / monthly): ").strip().lower()
        if value in GRANULARITY_DAYS:
            return value
        print("  [ERROR] Please choose daily, weekly or monthly.")


def compute_period_boundaries(
    report_type: str, start_date: str, end_date: str
) -> Tuple[Tuple[str, str], Tuple[str, str]]:
    """Return the current period and the previous comparable period."""
    current_start = datetime.strptime(start_date, "%Y-%m-%d")
    current_end = datetime.strptime(end_date, "%Y-%m-%d")
    period_len = (current_end - current_start).days + 1
    prev_end = current_start - timedelta(days=1)
    prev_start = prev_end - timedelta(days=period_len - 1)
    return (
        (start_date, end_date),
        (
            prev_start.strftime("%Y-%m-%d"),
            prev_end.strftime("%Y-%m-%d"),
        ),
    )


def fetch_period_summary(
    conn, start_date: str, end_date: str
) -> Dict[str, Optional[object]]:
    """Compute orders, revenue, unique customers, and top products for a period."""
    summary: Dict[str, Optional[object]] = {}

    cursor = conn.execute(
        """
        SELECT
            COUNT(DISTINCT o.order_id)                         AS total_orders,
            ROUND(SUM(oi.quantity * oi.unit_price
                      * (1 - oi.discount_percent / 100.0)), 2) AS total_revenue,
            COUNT(DISTINCT CASE WHEN o.customer_id != 'UNKNOWN'
                                THEN o.customer_id END)        AS unique_customers
        FROM orders o
        JOIN order_items oi ON o.order_id = oi.order_id
        WHERE date(o.order_date) BETWEEN ? AND ?
        """,
        (start_date, end_date),
    )
    row = cursor.fetchone()
    summary["total_orders"] = row["total_orders"] or 0
    summary["total_revenue"] = row["total_revenue"] or 0.0
    summary["unique_customers"] = row["unique_customers"] or 0

    cursor = conn.execute(
        """
        SELECT
            p.product_name,
            ROUND(SUM(oi.quantity * oi.unit_price
                      * (1 - oi.discount_percent / 100.0)), 2) AS product_revenue
        FROM order_items oi
        JOIN orders o    ON oi.order_id = o.order_id
        JOIN products p  ON oi.product_id = p.product_id
        WHERE date(o.order_date) BETWEEN ? AND ?
        GROUP BY p.product_id, p.product_name
        ORDER BY product_revenue DESC
        LIMIT 3
        """,
        (start_date, end_date),
    )
    summary["top_products"] = [
        (r["product_name"], r["product_revenue"]) for r in cursor.fetchall()
    ]

    return summary


def pct_change(current: float, previous: float) -> Optional[float]:
    """Compute percentage change, or None when previous is zero."""
    if previous == 0:
        return None
    return round((current - previous) * 100.0 / previous, 2)


def build_report_text(
    report_type: str,
    current_period: Tuple[str, str],
    previous_period: Tuple[str, str],
    current: Dict[str, Optional[object]],
    previous: Dict[str, Optional[object]],
) -> str:
    """Format the full report as a readable text block."""
    lines: List[str] = []
    lines.append(SEPARATOR)
    lines.append("E-COMMERCE ORDER ANALYTICS - SUMMARY REPORT")
    lines.append(f"Report granularity : {report_type.upper()}")
    lines.append(f"Period             : {current_period[0]}  to  {current_period[1]}")
    lines.append(
        f"Generated on       : {datetime.now().strftime(utils.CANONICAL_DATETIME_FORMAT)}"
    )
    lines.append(SEPARATOR)

    lines.append("")
    lines.append("KEY METRICS")
    lines.append("-" * 50)

    metrics = [
        ("Total orders", current["total_orders"], previous["total_orders"]),
        ("Total revenue", current["total_revenue"], previous["total_revenue"]),
        ("Unique customers", current["unique_customers"], previous["unique_customers"]),
    ]

    for label, cur, prev in metrics:
        change = pct_change(float(cur), float(prev))
        change_text = "-" if change is None else f"{change:+.2f}%"
        lines.append(
            f"  {label:<18}: {cur:>12}   (previous: {prev:>12}  |  {change_text})"
        )

    lines.append("")
    lines.append("TOP 3 PRODUCTS BY REVENUE")
    lines.append("-" * 50)
    current_products: List[Tuple[str, float]] = current["top_products"] or []
    previous_products: List[Tuple[str, float]] = previous["top_products"] or []
    previous_map = {name: rev for name, rev in previous_products}

    if not current_products:
        lines.append("  (no sales in this period)")
    for rank, (name, rev) in enumerate(current_products, start=1):
        prev_rev = previous_map.get(name)
        change_text = "-"
        if prev_rev is not None:
            change = pct_change(float(rev), float(prev_rev))
            change_text = "-" if change is None else f"{change:+.2f}%"
        lines.append(
            f"  {rank}. {name:<35} revenue: {rev:>10.2f}   "
            f"(prev: {prev_rev if prev_rev is not None else '-':>10} | {change_text})"
        )

    lines.append("")
    lines.append("PERIOD COMPARISON")
    lines.append("-" * 50)
    lines.append(
        f"  Previous comparable period: {previous_period[0]}  to  {previous_period[1]}"
    )

    revenue_change = pct_change(
        float(current["total_revenue"]), float(previous["total_revenue"])
    )
    orders_change = pct_change(
        float(current["total_orders"]), float(previous["total_orders"])
    )
    customers_change = pct_change(
        float(current["unique_customers"]), float(previous["unique_customers"])
    )

    def fmt(value: Optional[float]) -> str:
        if value is None:
            return "N/A (no previous data)"
        return f"{value:+.2f}%"

    lines.append(f"  Revenue change   : {fmt(revenue_change)}")
    lines.append(f"  Orders change    : {fmt(orders_change)}")
    lines.append(f"  Customers change : {fmt(customers_change)}")

    lines.append("")
    lines.append(SEPARATOR)
    lines.append("END OF REPORT")
    lines.append(SEPARATOR)

    return "\n".join(lines)


def run_demo_mode(conn) -> Path:
    """Generate the sample report for the last 30 days and save it."""
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=29)).strftime("%Y-%m-%d")

    current_period, previous_period = compute_period_boundaries(
        "monthly", start_date, end_date
    )

    current = fetch_period_summary(conn, *current_period)
    previous = fetch_period_summary(conn, *previous_period)

    body = build_report_text(
        "monthly", current_period, previous_period, current, previous
    )
    print(body)

    report_path = utils.report_file("sample_report.txt")
    report_path.write_text(body + "\n", encoding="utf-8")
    return report_path


def run_interactive(conn) -> Path:
    """Prompt the user and print/save a report to reports/last_report.txt."""
    print(SEPARATOR)
    print("E-COMMERCE ORDER ANALYTICS - CLI REPORT TOOL")
    print("Use Ctrl+C at any prompt to exit.")
    print(SEPARATOR)

    report_type = ask_for_report_type()
    start_date, end_date = ask_for_dates()

    current_period, previous_period = compute_period_boundaries(
        report_type, start_date, end_date
    )

    current = fetch_period_summary(conn, *current_period)
    previous = fetch_period_summary(conn, *previous_period)

    body = build_report_text(
        report_type, current_period, previous_period, current, previous
    )
    print(body)

    report_path = utils.report_file("last_report.txt")
    report_path.write_text(body + "\n", encoding="utf-8")
    print(f"Report saved to: {report_path}")
    return report_path


def main() -> None:
    """Entry point: run the CLI tool in interactive or demo mode."""
    parser = argparse.ArgumentParser(
        description="Generate an order analytics summary report from SQLite."
    )
    parser.add_argument(
        "--demo",
        action="store_true",
        help="Generate the sample report (reports/sample_report.txt) without prompts.",
    )
    args = parser.parse_args()

    if not utils.DB_PATH.exists():
        print(f"ERROR: database not found at {utils.DB_PATH}")
        print("Run src/load_database.py first.")
        sys.exit(1)

    conn = utils.get_connection(utils.DB_PATH)
    try:
        if args.demo:
            report_path = run_demo_mode(conn)
            print(f"Sample report written to: {report_path}")
        else:
            run_interactive(conn)
    finally:
        conn.close()


if __name__ == "__main__":
    main()