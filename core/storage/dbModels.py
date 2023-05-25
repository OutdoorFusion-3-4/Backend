import peewee
import pkg.storage.database as Database
import os
os.environ['db'] = 'database.db'
class BaseModel(peewee.Model):
    class Meta:
        database = peewee.SqliteDatabase(os.environ['db'])


class Company(BaseModel):
    company_id = peewee.AutoField()
    company_name = peewee.CharField()


class Product(BaseModel):
    product_id = peewee.AutoField()
    product_name = peewee.CharField(null=False)
    description = peewee.CharField(null=True)
    product_sale_price = peewee.FloatField(null=True)
    product_cost_price = peewee.FloatField(null=True)
    company = peewee.ForeignKeyField(Company, backref='products')


class Category(BaseModel):
    category_id = peewee.AutoField()
    name = peewee.CharField()


class ProductCategory(BaseModel):
    product = peewee.ForeignKeyField(Product)
    category = peewee.ForeignKeyField(Category)
    primary_key = peewee.CompositeKey('product', 'category')


class Customer(BaseModel):
    customer_id = peewee.AutoField()
    name = peewee.CharField(null=True)
    country = peewee.CharField(null=True)
    birthday = peewee.DateField(null=True)
    gender = peewee.CharField(null=True)


class OrderMethod(BaseModel):
    order_method_id = peewee.AutoField()
    order_method_name = peewee.CharField()


class Order(BaseModel):
    order_id = peewee.AutoField()
    order_date = peewee.DateField(null=True)
    order_method = peewee.ForeignKeyField(OrderMethod, null=True, backref='orders')
    customer = peewee.ForeignKeyField(Customer, null=True, backref='orders')


class OrderProduct(BaseModel):
    order_product_id = peewee.AutoField()
    quantity = peewee.IntegerField(null=True)
    order = peewee.ForeignKeyField(Order, backref='order_products')
    product = peewee.ForeignKeyField(Product, backref='order_products')
