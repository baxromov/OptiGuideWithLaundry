import asyncio
import random

from faker import Faker
from tortoise import Tortoise

from models import Customer, LaundryItem, Order, WashType, OrderItem, Inspection

fake = Faker()


async def init():
    await Tortoise.init(
        db_url='sqlite://db.sqlite3',
        modules={'models': ['models']}
    )
    await Tortoise.generate_schemas()


async def seed_data():
    materials = ['Cotton', 'Wool', 'Polyester', 'Silk', 'Linen', 'Denim', 'Nylon']
    item_names = ['Shirt', 'Pants', 'Jacket', 'Dress', 'Skirt', 'Blouse', 'T-shirt', 'Sweater', 'Shorts', 'Suit']
    wash_type_names = [
        ('Standard Wash', 'General purpose wash for most clothes'),
        ('Delicate Wash', 'Low agitation and low temperature for delicate fabrics'),
        ('Dry Clean', 'For sensitive fabrics, cleaned without water'),
        ('Heavy Duty', 'Extra wash for soiled items like workwear'),
        ('Eco Wash', 'Low water and energy consumption')
    ]

    wash_types = []
    laundry_items = []

    # Create wash types
    for name, desc in wash_type_names:
        wt = await WashType.create(
            name=name,
            description=desc,
            extra_price=str(round(random.uniform(0.5, 4.0), 2))
        )
        wash_types.append(wt)

    # Create laundry items
    for name in item_names:
        li = await LaundryItem.create(
            name=name,
            material=random.choice(materials),
            base_price=str(round(random.uniform(2.0, 15.0), 2))
        )
        laundry_items.append(li)

    # Create customers, orders, items and inspections
    for _ in range(1000):
        customer = await Customer.create(
            full_name=fake.name(),
            phone_number=fake.msisdn()[:20],
            address=fake.address()
        )

        order = await Order.create(
            customer=customer,
            total_price="0.0"
        )

        order_total = 0.0
        for _ in range(random.randint(1, 4)):
            laundry_item = random.choice(laundry_items)
            wash_type = random.choice(wash_types)
            quantity = random.randint(1, 5)

            item_base = float(laundry_item.base_price)
            extra = float(wash_type.extra_price)
            item_price = round(item_base + extra, 2)
            total_price = round(item_price * quantity, 2)

            order_item = await OrderItem.create(
                quantity=quantity,
                item_price=str(item_price),
                total_price=str(total_price),
                laundry_item=laundry_item,
                order=order,
                wash_type=wash_type
            )

            await Inspection.create(
                stains=random.randint(0, 3),
                damages=random.randint(0, 2),
                notes=fake.sentence(),
                order_item=order_item
            )

            order_total += total_price

        order.total_price = str(round(order_total, 2))
        await order.save()


if __name__ == '__main__':
    asyncio.run(init())
    asyncio.run(seed_data())
