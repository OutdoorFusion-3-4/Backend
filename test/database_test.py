
import datetime
import peewee
from pkg.queries.DataQueries import DataQueries
from pkg.queries.types import GraphQueryParameters
from core.storage.dbModels import Company, Product, Category, ProductCategory, Customer, Order, OrderProduct, OrderMethod
import core.storage.database as db
import unittest
import os


class TestDatabase (db.IDatabase):
    def __init__(self) -> None:
        test_db = 'test.db'
        os.environ['db'] = test_db
        self.db = peewee.SqliteDatabase(test_db)
        self.__setup()

    def getDatabaseConnection(self):
        return self.db

    def teardown(self):
        self.close_connection()
        self.db.drop_tables([Company, Product, Category, ProductCategory,
                             Customer, Order, OrderProduct, OrderMethod])

    def close_connection(self):
        self.db.close()

    def start_connection(self):
        self.db.connect()
        return self

    def __setup(self):
        self.start_connection()
        self.db.create_tables([Company, Product, Category, ProductCategory,
                               Customer, Order, OrderProduct, OrderMethod])
        self.__seed()
        self.close_connection()
        return self.db

    def __seed(self):
        companies = [
            {Company.company_name: 'Amazon'},
            {Company.company_name: 'Apple'},
        ]
        Company.insert_many(companies).execute()
        products = [
            {Product.product_name: 'echo dot', Product.description: 'echo dot',
                Product.product_sale_price: 50, Product.product_cost_price: 30, Product.company: 1},
            {Product.product_name: 'echo dot 2', Product.description: 'echo dot 2',
                Product.product_sale_price: 60, Product.product_cost_price: 40, Product.company: 1},
            {Product.product_name: 'iPhone 12', Product.description: 'iPhone 12',
                Product.product_sale_price: 1000, Product.product_cost_price: 800, Product.company: 2},
            {Product.product_name: 'iPhone 11', Product.description: 'iPhone 11',
                Product.product_sale_price: 900, Product.product_cost_price: 700, Product.company: 2},
        ]
        Product.insert_many(products).execute()
        categories = [
            {Category.name: 'Electronics'},
            {Category.name: 'Home'},
            {Category.name: 'Phones'},
        ]
        Category.insert_many(categories).execute()
        product_categories = [
            # echo dots
            {ProductCategory.product: 1, ProductCategory.category: 1},
            {ProductCategory.product: 1, ProductCategory.category: 2},
            {ProductCategory.product: 2, ProductCategory.category: 1},
            {ProductCategory.product: 2, ProductCategory.category: 2},
            # iPhones
            {ProductCategory.product: 3, ProductCategory.category: 1},
            {ProductCategory.product: 3, ProductCategory.category: 3},
            {ProductCategory.product: 4, ProductCategory.category: 1},
            {ProductCategory.product: 4, ProductCategory.category: 3},
        ]
        ProductCategory.insert_many(product_categories).execute()
        customers = [
            {Customer.name: 'John Doe', Customer.country: 'USA',
                Customer.birthday: '', Customer.gender: 'male'},
            {Customer.name: 'Anita Pea', Customer.country: 'Canada',
                Customer.birthday: '', Customer.gender: 'female'}
        ]
        Customer.insert_many(customers).execute()
        order_methods = [
            {OrderMethod.order_method_name: 'Online'},
            {OrderMethod.order_method_name: 'In Person'},
        ]
        OrderMethod.insert_many(order_methods).execute()
        orders = [
            {Order.customer: 1, Order.order_method: 1,
                Order.order_date: '2021-01-01'},
            {Order.customer: 1, Order.order_method: 2,
                Order.order_date: '2021-01-01'},
            {Order.customer: 2, Order.order_method: 1,
                Order.order_date: '2021-01-02'},
            {Order.customer: 2, Order.order_method: 2,
                Order.order_date: '2021-01-02'},
        ]
        Order.insert_many(orders).execute()
        order_products = [
            # buy from amazon
            {OrderProduct.order: 1, OrderProduct.product: 1, OrderProduct.quantity: 1},
            {OrderProduct.order: 1, OrderProduct.product: 2, OrderProduct.quantity: 1},
            # buy from apple
            {OrderProduct.order: 2, OrderProduct.product: 3, OrderProduct.quantity: 1},
            {OrderProduct.order: 2, OrderProduct.product: 4, OrderProduct.quantity: 1},
            # buy from amazon
            {OrderProduct.order: 3, OrderProduct.product: 1, OrderProduct.quantity: 1},
            {OrderProduct.order: 3, OrderProduct.product: 2, OrderProduct.quantity: 1},
            # buy from apple
            {OrderProduct.order: 4, OrderProduct.product: 3, OrderProduct.quantity: 1},
            {OrderProduct.order: 4, OrderProduct.product: 4, OrderProduct.quantity: 1},
        ]
        OrderProduct.insert_many(order_products).execute()
        return self


class Test_DataQueries(unittest.TestCase):
    def test_RevenuesByDate(self):
        db = TestDatabase()
        params = GraphQueryParameters()
        params.dateStart = datetime.date(2021, 1, 1).isoformat()
        params.dateEnd = datetime.date(2021, 1, 2).isoformat()
        params.companies = [1]
        try:
           res = DataQueries(db, params).Revenues()
           self.assertEqual(res.result, 220.0)
           self.assertEqual(len(res.resultPerDate), 4)
        except Exception as e:
            self.fail(e)
        finally:
            db.teardown()

    def test_RevenuesWithoutDate(self):
        db = TestDatabase()
        params = GraphQueryParameters()
        params.companies = [2]
        print('params:', params.companies)
        print(params)
        try:
           res = DataQueries(db, params).Revenues()
           self.assertEqual(res.result, 3800.0)
           self.assertEqual(len(res.resultPerDate), 4)
        except Exception as e:
            self.fail(e)
        finally:
            db.teardown()

    def test_ProfitsByDate(self):
        db = TestDatabase()
        params = GraphQueryParameters()
        params.dateStart = datetime.date(2021, 1, 1).isoformat()
        params.dateEnd = datetime.date(2021, 1, 2).isoformat()
        params.companies = [1]
        try:
           res = DataQueries(db, params).Profits()
           self.assertEqual(res.result, 80.0)
           self.assertEqual(len(res.resultPerDate), 4)
        except Exception as e:
            self.fail(e)
        finally:
            db.teardown()

    def test_ProfitsWithoutDate(self):
        db = TestDatabase()
        params = GraphQueryParameters()
        params.companies = [2]
        try:
           res = DataQueries(db, params).Profits()
           self.assertEqual(res.result, 800.0)
           self.assertEqual(len(res.resultPerDate), 4)
        except Exception as e:
            self.fail(e)
        finally:
            db.teardown()

    def test_OrdersByDate(self):
        db = TestDatabase()
        params = GraphQueryParameters()
        params.dateStart = datetime.date(2021, 1, 1).isoformat()
        params.dateEnd = datetime.date(2021, 1, 2).isoformat()
        params.companies = [1]
        try:
           res = DataQueries(db, params).Orders()
           self.assertEqual(res[0].Amount, 8)
        except Exception as e:
            self.fail(e)
        finally:
            db.teardown()

    def test_OrdersMultipleCompaniesNoDate(self):
        db = TestDatabase()
        params = GraphQueryParameters()
        params.companies = [1, 2]
        try:
           res = DataQueries(db, params).Orders()
           self.assertEqual(res[0].Amount, 20)
        except Exception as e:
            self.fail(e)
        finally:
            db.teardown()

    def test_CategoriesMultipleCompaniesNoDate(self):
        db = TestDatabase()
        params = GraphQueryParameters()
        params.companies = [1, 2]
        try:
           res = DataQueries(db, params).Categories()
           self.assertEqual(len(res), 3)
        except Exception as e:
            self.fail(e)
        finally:
            db.teardown()

    def test_OrderMethods(self):
        db = TestDatabase()
        params = GraphQueryParameters()
        params.companies = [1, 2]
        try:
           res = DataQueries(db, params).OrderMethods()
           self.assertEqual(len(res), 2)
        except Exception as e:
            self.fail(e)
        finally:
            db.teardown()

    def test_Products(self):
        db = TestDatabase()
        params = GraphQueryParameters()
        params.companies = [1, 2]
        try:
           res = DataQueries(db, params).Products()
           self.assertEqual(len(res), 4)
        except Exception as e:
            self.fail(e)
        finally:
            db.teardown()
    def test_Countries(self):
        db = TestDatabase()
        params = GraphQueryParameters()
        params.companies = [1, 2]
        try:
           res = DataQueries(db, params).Countries()
           self.assertEqual(len(res), 2)
        except Exception as e:
            self.fail(e)
        finally:
            db.teardown()


if __name__ == '__main__':
    unittest.main()
