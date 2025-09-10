TAX_RATE = 0.2  # глобальний стан 

 

def process_orders(orders, min_total, discount): 

    # orders: список словників {'id': int, 'items': [{'price': float, 'qty': int}], 'paid': bool} 

    valid = [] 

    total_revenue = 0.0 

 

    for o in orders: 

        if not o["paid"]: 

            continue 

        # побічний ефект 

        print("Processing order:", o["id"]) 

 

        # мутація 

        order_total = 0.0 

        for it in o["items"]: 

            order_total += it["price"] * it["qty"] 

        if order_total < min_total: 

            continue 

 

        # ще мутації і глобал TAX_RATE 

        order_total = order_total * (1 - discount) 

        order_total = order_total * (1 + TAX_RATE) 

 

        o["total"] = order_total  # мутуємо вхідні дані 

        valid.append(o) 

        total_revenue += order_total 

 

    return {"count": len(valid), "revenue": total_revenue, "orders": valid} 