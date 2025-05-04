from tortoise import fields, models


class Customer(models.Model):
    id = fields.IntField(pk=True)
    full_name = fields.CharField(max_length=100)
    phone_number = fields.CharField(max_length=20, null=True)
    address = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "customers"


class LaundryItem(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=100)
    material = fields.CharField(max_length=50, null=True)
    base_price = fields.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        table = "laundry_items"


class WashType(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    description = fields.TextField(null=True)
    extra_price = fields.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        table = "wash_types"


class Order(models.Model):
    id = fields.IntField(pk=True)
    customer = fields.ForeignKeyField('models.Customer', related_name='orders')
    total_price = fields.DecimalField(max_digits=10, decimal_places=2, null=True)
    status = fields.CharField(max_length=20, default='pending')
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "orders"


class OrderItem(models.Model):
    id = fields.IntField(pk=True)
    order = fields.ForeignKeyField('models.Order', related_name='order_items')
    laundry_item = fields.ForeignKeyField('models.LaundryItem', related_name='order_items')
    wash_type = fields.ForeignKeyField('models.WashType', related_name='order_items')
    quantity = fields.IntField()
    item_price = fields.DecimalField(max_digits=10, decimal_places=2)
    total_price = fields.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        table = "order_items"


class Inspection(models.Model):
    id = fields.IntField(pk=True)
    order_item = fields.ForeignKeyField('models.OrderItem', related_name='inspections')
    stains = fields.BooleanField(default=False)
    damages = fields.BooleanField(default=False)
    notes = fields.TextField(null=True)

    class Meta:
        table = "inspections"
