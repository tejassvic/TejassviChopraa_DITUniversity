"""
Phase 2 - Clean the raw CSV data and generate a cleaning report.
"""

from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src import utils  # noqa: E402

SEPARATOR = "=" * 70


def _clean_text(value: object) -> str:
    """Return a stripped string representation of a cell value."""
    if pd.isna(value):
        return ""
    return str(value).strip()


def clean_orders(raw_orders: pd.DataFrame) -> pd.DataFrame:
    """Clean order dates (canonical format), drop impossible dates, fill missing customer_ids."""
    df = raw_orders.copy()

    # Detect wrong-format dates.
    wrong_format_dates = []
    for idx, value in df["order_date"].items():
        text = _clean_text(value)
        try:
            datetime.strptime(text, utils.CANONICAL_DATETIME_FORMAT)
        except ValueError:
            if text:
                wrong_format_dates.append(idx)
    df["_wrong_date_format"] = False
    df.loc[wrong_format_dates, "_wrong_date_format"] = True

    # Convert all dates to canonical format.
    parsed_dates: List[datetime] = []
    unparseable_idx: List[int] = []

    for idx, value in df["order_date"].items():
        dt = utils.parse_datetime_loose(_clean_text(value))
        if dt is None:
            unparseable_idx.append(idx)
            parsed_dates.append(None)
        else:
            parsed_dates.append(dt)

    df["_parsed_date"] = parsed_dates

    # Remove impossible dates.
    dropped_impossible = len(unparseable_idx)
    if dropped_impossible:
        df = df.drop(index=unparseable_idx)

    df["order_date"] = df["_parsed_date"].apply(utils.format_datetime)
    df = df.drop(columns=["_parsed_date"])

    # Handle missing customer_id.
    df["customer_id"] = df["customer_id"].apply(_clean_text)
    missing_customer = (df["customer_id"] == "") | df["customer_id"].isna()
    df.loc[missing_customer, "customer_id"] = "UNKNOWN"

    _CLEAN_ISSUE_COUNTS["orders_wrong_date_format"] = int(df["_wrong_date_format"].sum())
    _CLEAN_ISSUE_COUNTS["orders_impossible_dates"] = dropped_impossible
    _CLEAN_ISSUE_COUNTS["orders_missing_customer_ids"] = int(missing_customer.sum())

    df = df.drop(columns=["_wrong_date_format"])
    return df


def clean_products(raw_products: pd.DataFrame) -> pd.DataFrame:
    """Trim product name whitespace, normalise to Title Case, and deduplicate."""
    df = raw_products.copy()

    original_names = df["product_name"].astype(str)

    # Trim and collapse whitespace.
    df["product_name"] = (
        df["product_name"]
        .astype(str)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )

    # Normalise to Title Case.
    df["product_name"] = df["product_name"].str.title()

    names_trimmed = int(
        (df["product_name"].str.strip() != original_names.str.strip()).sum()
    )
    _CLEAN_ISSUE_COUNTS["products_names_trimmed"] = names_trimmed

    # Remove accidental duplicates.
    before = len(df)
    df = df.drop_duplicates(subset=["product_name", "category"], keep="first")
    duplicates_removed = before - len(df)
    _CLEAN_ISSUE_COUNTS["products_duplicates_removed"] = duplicates_removed

    return df


def validate_emails(customers: pd.DataFrame) -> List[str]:
    """Return a list of customer_ids with invalid emails."""
    invalid_ids: List[str] = []

    for _, row in customers.iterrows():
        email = _clean_text(row["email"])
        # Valid email must have exactly one '@' with non-empty parts.
        at_parts = email.split("@")
        if len(at_parts) != 2 or not at_parts[0] or not at_parts[1]:
            invalid_ids.append(str(row["customer_id"]))

    _CLEAN_ISSUE_COUNTS["customers_invalid_emails"] = len(invalid_ids)
    return invalid_ids


def check_referential_integrity(
    order_items: pd.DataFrame, orders: pd.DataFrame
) -> List[str]:
    """Return order_ids in items that do not exist in orders."""
    valid_order_ids: Set[str] = set(orders["order_id"].astype(str))
    orphaned: List[str] = []

    for order_id in order_items["order_id"]:
        oid = str(order_id).strip()
        if oid and oid not in valid_order_ids:
            orphaned.append(oid)

    _CLEAN_ISSUE_COUNTS["order_items_orphan_order_ids"] = len(orphaned)
    return orphaned


# Counts for every issue discovered during the pipeline.
_CLEAN_ISSUE_COUNTS: Dict[str, int] = {}


def write_cleaning_report(
    raw_counts: Dict[str, int],
    cleaned_counts: Dict[str, int],
    invalid_email_ids: List[str],
    orphaned_order_ids: List[str],
) -> None:
    """Write the cleaning report to reports/cleaning_report.txt."""
    report_path = utils.report_file("cleaning_report.txt")
    report_path.parent.mkdir(parents=True, exist_ok=True)

    lines: List[str] = []
    lines.append(SEPARATOR)
    lines.append("DATA CLEANING REPORT")
    lines.append(f"Generated on : {datetime.now().strftime(utils.CANONICAL_DATETIME_FORMAT)}")
    lines.append(SEPARATOR)

    lines.append("")
    lines.append("1. INPUT SUMMARY (raw files)")
    lines.append("-" * 50)
    for name, count in raw_counts.items():
        lines.append(f"   {name:<20} : {count:>6} rows")

    lines.append("")
    lines.append("2. ISSUES FOUND & RESOLVED")
    lines.append("-" * 50)

    issue_descriptions = {
        "orders_wrong_date_format": (
            "Orders with dates in the wrong format (DD-MM-YYYY) - converted"
        ),
        "orders_impossible_dates": (
            "Orders with impossible/unparseable dates - removed"
        ),
        "orders_missing_customer_ids": (
            "Orders with missing customer_id - set to 'UNKNOWN'"
        ),
        "products_names_trimmed": (
            "Product names with extra whitespace / bad casing - normalised"
        ),
        "products_duplicates_removed": (
            "Duplicate products - removed"
        ),
        "customers_invalid_emails": (
            "Customers with invalid emails - flagged"
        ),
        "order_items_orphan_order_ids": (
            "Order items referencing non-existent orders - flagged"
        ),
    }

    for key, description in issue_descriptions.items():
        count = _CLEAN_ISSUE_COUNTS.get(key, 0)
        lines.append(f"   * {description:<60} : {count:>5}")

    lines.append("")
    lines.append("3. CLEANED OUTPUT SUMMARY")
    lines.append("-" * 50)
    for name, count in cleaned_counts.items():
        lines.append(f"   {name:<20} : {count:>6} rows")

    lines.append("")
    lines.append("4. DETAILS")
    lines.append("-" * 50)

    lines.append(f"   Invalid email customer IDs ({len(invalid_email_ids)}):")
    if invalid_email_ids:
        lines.append("      " + ", ".join(invalid_email_ids[:20]) +
                     (" ..." if len(invalid_email_ids) > 20 else ""))
    else:
        lines.append("      (none)")

    lines.append("")
    lines.append(f"   Orphaned order IDs in items ({len(orphaned_order_ids)}):")
    if orphaned_order_ids:
        lines.append("      " + ", ".join(orphaned_order_ids[:20]) +
                     (" ..." if len(orphaned_order_ids) > 20 else ""))
    else:
        lines.append("      (none)")

    lines.append("")
    lines.append(SEPARATOR)
    lines.append("END OF REPORT")
    lines.append(SEPARATOR)

    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  [OK] Cleaning report written to {report_path}")


def save_cleaned_dataframes(dataframes: Dict[str, pd.DataFrame]) -> None:
    """Save each cleaned dataframe to data/cleaned/."""
    utils.CLEANED_DATA_DIR.mkdir(parents=True, exist_ok=True)

    for file_name, df in dataframes.items():
        path = utils.cleaned_csv(file_name)
        df.to_csv(path, index=False)
        print(f"  [OK] Saved {path}")


def main() -> None:
    """Entry point: run the cleaning pipeline and generate the report."""
    print(SEPARATOR)
    print("PHASE 2 - CLEANING RAW DATA")
    print(SEPARATOR)

    # Load raw files.
    raw_orders = pd.read_csv(utils.raw_csv(utils.ORDERS_CSV), dtype=str)
    raw_order_items = pd.read_csv(utils.raw_csv(utils.ORDER_ITEMS_CSV), dtype=str)
    raw_products = pd.read_csv(utils.raw_csv(utils.PRODUCTS_CSV), dtype=str)
    raw_customers = pd.read_csv(utils.raw_csv(utils.CUSTOMERS_CSV), dtype=str)

    raw_counts = {
        "orders.csv": len(raw_orders),
        "order_items.csv": len(raw_order_items),
        "products.csv": len(raw_products),
        "customers.csv": len(raw_customers),
    }

    # Clean each dataset.
    cleaned_orders = clean_orders(raw_orders)
    cleaned_products = clean_products(raw_products)
    cleaned_customers = raw_customers.copy()

    # Coerce numeric columns on order_items.
    cleaned_order_items = raw_order_items.copy()
    for col in ("quantity", "unit_price", "discount_percent"):
        cleaned_order_items[col] = pd.to_numeric(
            cleaned_order_items[col], errors="coerce"
        )
    # Drop rows where numeric conversion failed.
    numeric_issues = int(cleaned_order_items[["quantity", "unit_price", "discount_percent"]]
                         .isna().any(axis=1).sum())
    if numeric_issues:
        cleaned_order_items = cleaned_order_items.dropna(
            subset=["quantity", "unit_price", "discount_percent"]
        )
    _CLEAN_ISSUE_COUNTS["order_items_non_numeric_dropped"] = numeric_issues

    # Validation checks.
    invalid_email_ids = validate_emails(cleaned_customers)
    orphaned_order_ids = check_referential_integrity(
        cleaned_order_items, cleaned_orders
    )

    # Save cleaned files.
    save_cleaned_dataframes(
        {
            utils.ORDERS_CSV: cleaned_orders,
            utils.ORDER_ITEMS_CSV: cleaned_order_items,
            utils.PRODUCTS_CSV: cleaned_products,
            utils.CUSTOMERS_CSV: cleaned_customers,
        }
    )

    cleaned_counts = {
        "orders_cleaned.csv": len(cleaned_orders),
        "order_items_cleaned.csv": len(cleaned_order_items),
        "products_cleaned.csv": len(cleaned_products),
        "customers_cleaned.csv": len(cleaned_customers),
    }

    # Write report.
    write_cleaning_report(
        raw_counts=raw_counts,
        cleaned_counts=cleaned_counts,
        invalid_email_ids=invalid_email_ids,
        orphaned_order_ids=orphaned_order_ids,
    )

    print(SEPARATOR)
    print(f"Cleaning pipeline completed. {sum(cleaned_counts.values())} "
          f"rows written to data/cleaned/.")
    print(SEPARATOR)


if __name__ == "__main__":
    main()