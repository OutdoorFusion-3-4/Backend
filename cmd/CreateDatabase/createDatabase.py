import sys
sys.path.append('./')
import pkg.storage.database as Database
from core.storage.db import Company, Product, Category, ProductCategory, Customer, Order, OrderProduct

database = Database('outdoorfusion.db')
db = database.start_connection()

db.create_tables([Company, Product, Category, ProductCategory, Customer, Order, OrderProduct])

database.close_connection()