"""
Phase 1 - Generate raw (deliberately messy) CSV data.
"""

from __future__ import annotations

import random
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple

import pandas as pd
from faker import Faker

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src import utils  # noqa: E402

# Row counts
NUMBER_OF_ORDERS = 700
NUMBER_OF_PRODUCTS = 80
NUMBER_OF_CUSTOMERS = 150

MIN_ITEMS_PER_ORDER = 1
MAX_ITEMS_PER_ORDER = 5

# Data-quality issue probabilities
NULL_CUSTOMER_PROB = 0.05
NEGATIVE_QUANTITY_PROB = 0.03
WRONG_DATE_FORMAT_PROB = 0.08
EXTRA_SPACE_PROB = 0.10
MIXED_CASE_PROB = 0.10
INVALID_EMAIL_PROB = 0.02

ORDER_STATUSES = ["PLACED", "SHIPPED", "DELIVERED", "CANCELLED", "RETURNED"]
CUSTOMER_TYPES = ["REGULAR", "PREMIUM", "VIP"]
REGION_CODES = ["NORTH", "SOUTH", "EAST", "WEST", "CENTRAL"]

# (name, category, subcategory)
PRODUCT_CATALOGUE: List[Tuple[str, str, str]] = [
    ("Wireless Mouse", "Electronics", "Accessories"),
    ("Mechanical Keyboard", "Electronics", "Accessories"),
    ("27 Inch Monitor", "Electronics", "Displays"),
    ("USB-C Hub", "Electronics", "Accessories"),
    ("Noise Cancelling Headphones", "Electronics", "Audio"),
    ("Bluetooth Speaker", "Electronics", "Audio"),
    ("4K Webcam", "Electronics", "Accessories"),
    ("Laptop Stand", "Electronics", "Accessories"),
    ("Smart Watch", "Electronics", "Wearables"),
    ("Fitness Tracker", "Electronics", "Wearables"),
    ("External SSD 1TB", "Electronics", "Storage"),
    ("Wireless Charger", "Electronics", "Accessories"),
    ("Gaming Console", "Electronics", "Gaming"),
    ("VR Headset", "Electronics", "Gaming"),
    ("Smart Home Hub", "Electronics", "Smart Home"),
    ("WiFi Router", "Electronics", "Networking"),
    ("Tablet", "Electronics", "Computing"),
    ("E-Reader", "Electronics", "Computing"),
    ("Digital Camera", "Electronics", "Photography"),
    ("Portable Power Bank", "Electronics", "Accessories"),
    ("Cotton T-Shirt", "Clothing", "Men"),
    ("Denim Jeans", "Clothing", "Men"),
    ("Running Shoes", "Clothing", "Footwear"),
    ("Leather Jacket", "Clothing", "Men"),
    ("Wool Sweater", "Clothing", "Women"),
    ("Summer Dress", "Clothing", "Women"),
    ("Sports Leggings", "Clothing", "Women"),
    ("Windbreaker", "Clothing", "Outerwear"),
    ("Formal Shirt", "Clothing", "Men"),
    ("Knit Cardigan", "Clothing", "Women"),
    ("Sneakers", "Clothing", "Footwear"),
    ("Polo Shirt", "Clothing", "Men"),
    ("Chino Trousers", "Clothing", "Men"),
    ("Skirt", "Clothing", "Women"),
    ("Winter Gloves", "Clothing", "Accessories"),
    ("Beanie Hat", "Clothing", "Accessories"),
    ("Socks 5-Pack", "Clothing", "Accessories"),
    ("Belt", "Clothing", "Accessories"),
    ("Raincoat", "Clothing", "Outerwear"),
    ("Hoodie", "Clothing", "Men"),
    ("Non-Stick Frying Pan", "Home", "Kitchen"),
    ("Coffee Maker", "Home", "Kitchen"),
    ("Air Fryer", "Home", "Kitchen"),
    ("Toaster", "Home", "Kitchen"),
    ("Blender", "Home", "Kitchen"),
    ("Dinner Plate Set", "Home", "Kitchen"),
    ("Cutlery Set", "Home", "Kitchen"),
    ("Glass Storage Jars", "Home", "Kitchen"),
    ("Memory Foam Pillow", "Home", "Bedding"),
    ("Bed Sheet Set", "Home", "Bedding"),
    ("Duvet Cover", "Home", "Bedding"),
    ("Bath Towel Set", "Home", "Bathroom"),
    ("Shower Curtain", "Home", "Bathroom"),
    ("Scented Candle", "Home", "Decor"),
    ("Wall Clock", "Home", "Decor"),
    ("Table Lamp", "Home", "Lighting"),
    ("Floor Rug", "Home", "Decor"),
    ("Bookshelf", "Home", "Furniture"),
    ("Office Chair", "Home", "Furniture"),
    ("Foldable Desk", "Home", "Furniture"),
    ("Python Programming", "Books", "Technology"),
    ("SQL Essentials", "Books", "Technology"),
    ("Data Science Handbook", "Books", "Technology"),
    ("Machine Learning Basics", "Books", "Technology"),
    ("Clean Code", "Books", "Technology"),
    ("The Art of Statistics", "Books", "Mathematics"),
    ("Calculus Made Easy", "Books", "Mathematics"),
    ("Linear Algebra Primer", "Books", "Mathematics"),
    ("World History", "Books", "History"),
    ("Modern India", "Books", "History"),
    ("Bestseller Novel", "Books", "Fiction"),
    ("Sci-Fi Anthology", "Books", "Fiction"),
    ("Mystery Thriller", "Books", "Fiction"),
    ("Travel Photography", "Books", "Art"),
    ("Watercolor Guide", "Books", "Art"),
    ("Cooking Basics", "Books", "Cooking"),
    ("Baking for Beginners", "Books", "Cooking"),
    ("Yoga for Health", "Books", "Wellness"),
    ("Meditation Guide", "Books", "Wellness"),
    ("Biography of a Visionary", "Books", "Biography"),
]

SEPARATOR = "=" * 70


def generate_customers(faker: Faker, n: int) -> pd.DataFrame:
    """Generate the raw customers dataframe."""
    records: List[Dict] = []

    for i in range(1, n + 1):
        customer_id = f"CUST-{i:04d}"
        name = faker.name()
        email = f"{name.lower().replace(' ', '.').replace('.', '_', 1)}@{faker.free_email_domain()}"

        # 2% chance of an invalid email (missing @ or domain).
        if random.random() < INVALID_EMAIL_PROB:
            if random.random() < 0.5:
                email = email.replace("@", "")
            else:
                email = email.split("@")[0] + "@"

        records.append(
            {
                "customer_id": customer_id,
                "customer_name": name,
                "email": email,
                "registration_date": faker.date_between(start_date="-3y", end_date="today").strftime(
                    utils.CANONICAL_DATETIME_FORMAT
                ),
                "customer_type": random.choice(CUSTOMER_TYPES),
            }
        )

    return pd.DataFrame(records)


def generate_products(faker: Faker) -> pd.DataFrame:
    """Generate the raw products dataframe with spaced/cased names."""
    records: List[Dict] = []

    for i, (name, category, subcategory) in enumerate(PRODUCT_CATALOGUE, start=1):
        product_id = f"PRD-{i:04d}"
        product_name = name

        # 10% chance of extra spaces.
        if random.random() < EXTRA_SPACE_PROB:
            parts = product_name.split()
            product_name = "  " + "   ".join(parts) + "  " if len(parts) > 1 else " " + product_name + " "

        # 10% chance of mixed case.
        if random.random() < MIXED_CASE_PROB:
            product_name = "".join(
                c.upper() if random.random() < 0.5 else c.lower() for c in product_name
            )

        records.append(
            {
                "product_id": product_id,
                "product_name": product_name,
                "category": category,
                "subcategory": subcategory,
                "cost_price": round(random.uniform(5.0, 500.0), 2),
            }
        )

    return pd.DataFrame(records)


def _random_order_date(faker: Faker) -> Tuple[str, bool]:
    """Generate an order date; ~8% use the wrong DD-MM-YYYY format."""
    days_ago = random.randint(0, 548)
    dt = datetime.now() - timedelta(days=days_ago)

    if random.random() < WRONG_DATE_FORMAT_PROB:
        return dt.strftime(utils.WRONG_DATETIME_FORMAT), True

    dt = dt.replace(
        hour=random.randint(0, 23),
        minute=random.randint(0, 59),
        second=random.randint(0, 59),
    )
    return dt.strftime(utils.CANONICAL_DATETIME_FORMAT), False


def generate_orders(faker: Faker, n: int, customer_ids: List[str]) -> pd.DataFrame:
    """Generate the raw orders dataframe with missing customer references."""
    records: List[Dict] = []
    null_customer_counter = 0
    wrong_date_counter = 0

    for i in range(1, n + 1):
        order_id = f"ORD-{i:05d}"

        # 5% of orders lose their customer reference.
        if random.random() < NULL_CUSTOMER_PROB:
            customer_id = ""
            null_customer_counter += 1
        else:
            customer_id = random.choice(customer_ids)

        order_date, wrong = _random_order_date(faker)
        if wrong:
            wrong_date_counter += 1

        records.append(
            {
                "order_id": order_id,
                "customer_id": customer_id,
                "order_date": order_date,
                "status": random.choice(ORDER_STATUSES),
                "region_code": random.choice(REGION_CODES),
            }
        )

    global _RAW_ORDER_ISSUE_COUNTS
    _RAW_ORDER_ISSUE_COUNTS = {
        "null_customer": null_customer_counter,
        "wrong_date_format": wrong_date_counter,
    }

    return pd.DataFrame(records)


def generate_order_items(
    faker: Faker, orders: pd.DataFrame, product_ids: List[str]
) -> pd.DataFrame:
    """Generate raw order_items with valid order references."""
    records: List[Dict] = []
    negative_quantity_counter = 0
    item_counter = 1

    for _, order in orders.iterrows():
        number_of_items = random.randint(MIN_ITEMS_PER_ORDER, MAX_ITEMS_PER_ORDER)

        for _ in range(number_of_items):
            item_id = f"ITM-{item_counter:06d}"
            item_counter += 1

            quantity = random.randint(1, 5)
            # 3% of line items are returns (negative quantity).
            if random.random() < NEGATIVE_QUANTITY_PROB:
                quantity = -quantity
                negative_quantity_counter += 1

            records.append(
                {
                    "item_id": item_id,
                    "order_id": order["order_id"],
                    "product_id": random.choice(product_ids),
                    "quantity": quantity,
                    "unit_price": round(random.uniform(5.0, 800.0), 2),
                    "discount_percent": round(random.uniform(0.0, 60.0), 1),
                }
            )

    global _RAW_ITEM_ISSUE_COUNTS
    _RAW_ITEM_ISSUE_COUNTS = {"negative_quantity": negative_quantity_counter}

    return pd.DataFrame(records)


def save_dataframes(dataframes: Dict[str, pd.DataFrame]) -> None:
    """Save each dataframe to data/raw/."""
    utils.RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    for file_name, df in dataframes.items():
        path = utils.raw_csv(file_name)
        df.to_csv(path, index=False)
        print(f"  [OK] Saved {path}")


def print_generation_statistics(
    customers_n: int, products_n: int, orders_n: int, items_n: int
) -> None:
    """Print a summary of the generated data."""
    print()
    print(SEPARATOR)
    print("DATA GENERATION SUMMARY")
    print(SEPARATOR)
    print(f"  Customers generated : {customers_n}")
    print(f"  Products generated  : {products_n}")
    print(f"  Orders generated    : {orders_n}")
    print(f"  Order items         : {items_n}")
    print(f"  Regions covered     : {len(REGION_CODES)} ({', '.join(REGION_CODES)})")
    print("-" * 70)
    print("  Injected data-quality issues (raw):")
    print(f"    * Orders  with NULL customer_id  : {_RAW_ORDER_ISSUE_COUNTS['null_customer']} "
          f"({NULL_CUSTOMER_PROB:.0%})")
    print(f"    * Orders  with wrong date format : {_RAW_ORDER_ISSUE_COUNTS['wrong_date_format']} "
          f"(~{WRONG_DATE_FORMAT_PROB:.0%})")
    print(f"    * Items   with negative quantity : {_RAW_ITEM_ISSUE_COUNTS['negative_quantity']} "
          f"({NEGATIVE_QUANTITY_PROB:.0%})")
    print(f"    * Product names with extra spaces: ~{EXTRA_SPACE_PROB:.0%}")
    print(f"    * Product names in mixed case    : ~{MIXED_CASE_PROB:.0%}")
    print(f"    * Customers with invalid email   : ~{INVALID_EMAIL_PROB:.0%}")
    print(SEPARATOR)


_RAW_ORDER_ISSUE_COUNTS: Dict[str, int] = {}
_RAW_ITEM_ISSUE_COUNTS: Dict[str, int] = {}


def main() -> None:
    """Entry point: generate all four raw CSV files."""
    random.seed(42)
    faker = Faker()
    Faker.seed(42)

    print(SEPARATOR)
    print("PHASE 1 - GENERATING RAW DATA")
    print(SEPARATOR)

    customers = generate_customers(faker, NUMBER_OF_CUSTOMERS)
    products = generate_products(faker)
    product_ids = products["product_id"].tolist()

    customer_ids = customers["customer_id"].tolist()
    orders = generate_orders(faker, NUMBER_OF_ORDERS, customer_ids)
    order_items = generate_order_items(faker, orders, product_ids)

    save_dataframes(
        {
            utils.ORDERS_CSV: orders,
            utils.ORDER_ITEMS_CSV: order_items,
            utils.PRODUCTS_CSV: products,
            utils.CUSTOMERS_CSV: customers,
        }
    )

    print_generation_statistics(
        customers_n=len(customers),
        products_n=len(products),
        orders_n=len(orders),
        items_n=len(order_items),
    )

    # Final integrity check.
    valid_order_ids = set(orders["order_id"])
    orphaned = [oid for oid in order_items["order_id"] if oid not in valid_order_ids]
    if orphaned:
        raise RuntimeError(
            f"Referential integrity violation: {len(orphaned)} items "
            f"reference non-existent orders."
        )

    print("Referential integrity check : PASSED (all order_ids valid)")


if __name__ == "__main__":
    main()