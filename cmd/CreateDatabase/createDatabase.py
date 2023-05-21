from core.storage.dbModels import Company, Product, Category, ProductCategory, Customer, Order, OrderProduct, OrderMethod
import pkg.storage.database as Database
import sys
sys.path.append('./')

database = Database()
db = database.start_connection()

db.create_tables([Company, Product, Category, ProductCategory,
                 Customer, Order, OrderProduct, OrderMethod])

database.close_connection()