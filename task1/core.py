from __future__ import annotations

from typing import Callable, Iterable, List, Dict, TypedDict, TypeVar

# -----------------------------
# Типи (іммутабельні за домовленістю)
# -----------------------------


class Item(TypedDict):
    price: float
    qty: int


class Order(TypedDict, total=False):
    id: int
    items: List[Item]
    paid: bool
    total: float  # з'являється лише у вихідних даних


def order_subtotal(order: Order) -> float:
    return sum(it["price"] * it["qty"] for it in order["items"])


def with_total(order: Order, total: float) -> Order:
    # Повертаємо НОВИЙ словник, не мутуємо вхідні дані.
    return {**order, "total": total}


def process_orders_pure(
    orders: Iterable[Order],
    *,
    min_total: float,
    discount: float,
    tax_rate: float,
) -> Dict[str, object]:
    """
    Чисте ядро:
    - без I/O
    - без глобальних змінних
    - без мутацій вхідних структур
    """
    qualified: List[Order] = []
    revenue = 0.0

    for o in orders:
        if not o.get("paid", False):
            continue
        subtotal = order_subtotal(o)
        if subtotal < min_total:
            continue
        total = subtotal * (1 - discount)
        total *= 1 + tax_rate
        new_o = with_total(o, total)
        qualified.append(new_o)
        revenue += total

    return {"count": len(qualified), "revenue": revenue, "orders": qualified}


# -----------------------------
# Callable-політики (композиційність)
# -----------------------------

Subtotal = float
Amount = float

FilterFn = Callable[[Subtotal], bool]
DiscountFn = Callable[[Subtotal], Amount]
TaxFn = Callable[[Amount], Amount]
Processor = Callable[[List[Order]], Dict[str, object]]


def make_processor(
    *,
    accept: FilterFn,
    apply_discount: DiscountFn,
    apply_tax: TaxFn,
) -> Processor:
    def process(orders: List[Order]) -> Dict[str, object]:
        qualified: List[Order] = []
        revenue = 0.0
        for o in orders:
            if not o.get("paid", False):
                continue
            subtotal = order_subtotal(o)
            if not accept(subtotal):
                continue
            total = apply_tax(apply_discount(subtotal))
            qualified.append(with_total(o, total))
            revenue += total
        return {"count": len(qualified), "revenue": revenue, "orders": qualified}

    return process


# -----------------------------
# Маленькі утиліти композиції
# -----------------------------

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


def compose(f: Callable[[B], C], g: Callable[[A], B]) -> Callable[[A], C]:
    return lambda x: f(g(x))
