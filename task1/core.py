from typing import Iterable, Callable, TypedDict, List, Dict 

 

class Item(TypedDict): 

    price: float 

    qty: int 

 

class Order(TypedDict, total=False): 

    id: int 

    items: List[Item] 

    paid: bool 

    total: float  # з'явиться в результаті 

 

def order_subtotal(order: Order) -> float: 

    return sum(it["price"] * it["qty"] for it in order["items"]) 

 

def with_total(order: Order, total: float) -> Order: 

    # повертаємо НОВИЙ словник (вхідний не чіпаємо) 

    return {**order, "total": total} 

 

def process_orders_pure( 

    orders: Iterable[Order], 

    *, 

    min_total: float, 

    discount: float, 

    tax_rate: float 

) -> Dict[str, object]: 

    paid = (o for o in orders if o["paid"]) 

    qualified = [] 

    revenue = 0.0 

 

    for o in paid: 

        subtotal = order_subtotal(o) 

        if subtotal < min_total: 

            continue 

        total = subtotal * (1 - discount) 

        total = total * (1 + tax_rate) 

        new_o = with_total(o, total) 

        qualified.append(new_o) 

        revenue += total 

 

    return {"count": len(qualified), "revenue": revenue, "orders": qualified} 

# app.py — оболонка побічних ефектів 

from core import process_orders_pure 

 

def run(orders): 

    result = process_orders_pure(orders, min_total=100, discount=0.1, tax_rate=0.2) 

    for o in result["orders"]: 

        print("Processed:", o["id"], "total:", o["total"]) 

    print("Revenue:", result["revenue"]) 