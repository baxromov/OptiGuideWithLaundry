from datetime import date

from models import Order


async def fetch_wash_type_data():
    today = date.today()
    orders_today = await Order.all().prefetch_related("order_items__laundry_item", "order_items__wash_type")

    wash_type_data = {}

    for order in orders_today:
        for item in order.order_items:
            wt_id = item.wash_type.id
            qty = item.quantity
            base_price = float(item.laundry_item.base_price)
            extra_price = float(item.wash_type.extra_price)
            price_per_item = base_price + extra_price
            revenue = price_per_item * qty

            if wt_id not in wash_type_data:
                wash_type_data[wt_id] = {
                    "wash_type_name": item.wash_type.name,
                    "total_quantity": 0,
                    "total_revenue": 0.0,
                    "capacity": 10  # Example fixed capacity, or fetch from DB if available
                }
            wash_type_data[wt_id]["total_quantity"] += qty
            wash_type_data[wt_id]["total_revenue"] += revenue

    return wash_type_data
