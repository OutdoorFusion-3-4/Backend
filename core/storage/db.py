import peewee
import pymysql

pymysql.install_as_MySQLdb()

db = peewee.MySQLDatabase('outdoorfusion', host='localhost', port=3306, user='root', password='Appelsap123!')

class BaseModel(peewee.Model):
    class Meta:
        database = db

class Company(BaseModel):
    company_id = peewee.PrimaryKeyField()
    company_name = peewee.CharField()

class Product(BaseModel):
    product_id = peewee.PrimaryKeyField()
    product_name = peewee.CharField(null=False)
    description = peewee.CharField()
    product_sale_price = peewee.DoubleField()
    product_cost_price = peewee.DoubleField()
    company = peewee.ForeignKeyField(Company, backref='products')

class Category(BaseModel):
    category_id = peewee.PrimaryKeyField()
    name = peewee.CharField()

class ProductCategory(BaseModel):
    product = peewee.ForeignKeyField(Product)
    category = peewee.ForeignKeyField(Category)
    primary_key = peewee.CompositeKey('product', 'category')

class Customer(BaseModel):
    customer_id = peewee.PrimaryKeyField()
    name = peewee.CharField()
    country = peewee.CharField()
    birthday = peewee.DateField()
    gender = peewee.CharField()

class Order(BaseModel):
    order_id = peewee.PrimaryKeyField()
    order_date = peewee.DateField()
    customer = peewee.ForeignKeyField(Customer, backref='orders')

class OrderProduct(BaseModel):
    order_product_id = peewee.PrimaryKeyField()
    quantity = peewee.IntegerField()
    order = peewee.ForeignKeyField(Order, backref='order_products')
    product = peewee.ForeignKeyField(Product, backref='order_products')

# Tables creation
db.create_tables([Company, Product, Category, ProductCategory, Customer, Order, OrderProduct])
