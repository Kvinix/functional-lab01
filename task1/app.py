from __future__ import annotations

import argparse
from typing import List

from core import Order, process_orders_pure


def sample_orders() -> List[Order]:
    return [
        {"id": 1, "paid": True, "items": [{"price": 50.0, "qty": 2}, {"price": 20.0, "qty": 1}]},
        {"id": 2, "paid": False, "items": [{"price": 200.0, "qty": 1}]},
        {"id": 3, "paid": True, "items": [{"price": 30.0, "qty": 3}]},
    ]


def main() -> None:
    parser = argparse.ArgumentParser(description="Functional processing demo")
    parser.add_argument("--min-total", type=float, default=100.0)
    parser.add_argument("--discount", type=float, default=0.10)
    parser.add_argument("--tax", type=float, default=0.20)
    args = parser.parse_args()

    orders = sample_orders()
    result = process_orders_pure(
        orders,
        min_total=args.min_total,
        discount=args.discount,
        tax_rate=args.tax,
    )

    for o in result["orders"]:
        print(f"Processed id={o['id']} total={o['total']:.2f}")
    print(f"Revenue: {result['revenue']:.2f}")


if __name__ == "__main__":
    main()
