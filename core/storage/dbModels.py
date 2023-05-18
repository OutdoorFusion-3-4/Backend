import peewee
import pkg.storage.database as Database

class BaseModel(peewee.Model):
    class Meta:
        database = Database().getDatabase()

class Company(BaseModel):
    company_id = peewee.AutoField()
    company_name = peewee.CharField()

class Product(BaseModel):
    product_id = peewee.AutoField()
    product_name = peewee.CharField(null=False)
    description = peewee.CharField()
    product_sale_price = peewee.FloatField()
    product_cost_price = peewee.FloatField()
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
    name = peewee.CharField()
    country = peewee.CharField()
    birthday = peewee.DateField()
    gender = peewee.CharField()
class OrderMethod(BaseModel):
    order_method_id = peewee.AutoField()
    order_method_name = peewee.CharField()

class Order(BaseModel):
    order_id = peewee.AutoField()
    order_date = peewee.DateField()
    order_method = peewee.ForeignKeyField(OrderMethod, backref='orders')
    customer = peewee.ForeignKeyField(Customer, backref='orders')

class OrderProduct(BaseModel):
    order_product_id = peewee.AutoField()
    quantity = peewee.IntegerField()
    order = peewee.ForeignKeyField(Order, backref='order_products')
    product = peewee.ForeignKeyField(Product, backref='order_products')



