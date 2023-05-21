import sys
sys.path.append('./')
import os
os.environ['db'] = 'database.db'

from core.storage.dbModels import Company, Product, Category, ProductCategory, Customer, Order, OrderProduct, OrderMethod
from pkg.storage.database import Database

def main():
    database = Database()
    db = database.start_connection()

    db.create_tables([Company, Product, Category, ProductCategory,
                    Customer, Order, OrderProduct, OrderMethod])

    database.close_connection()

if __name__ == '__main__':
    main()
