from core.storage.database import IDatabase
from core.storage.dbModels import Category, OrderMethod, Product, Order, OrderProduct, ProductCategory, Customer
from queries.types import GraphQueryParameters, Results
from queries.baseQueries import BaseQueries
from peewee import fn


class DataQueries (BaseQueries):
    def __init__(self, dbConnection: IDatabase, parameters: GraphQueryParameters):
        self.dbConnection = dbConnection
        self.parameters = parameters

        # transform iso string to datetime object
        self.parameters.dateStart = self.from_iso_string(
            self.parameters.dateStart)
        self.parameters.dateEnd = self.from_iso_string(self.parameters.dateEnd)

    def Revenues(self) -> Results:
        self.dbConnection.start_connection()
        query = (Order.select(Order.order_date, OrderProduct.quantity, Product.product_sale_price)
                 .join(OrderProduct)
                 .join(Product)
                 .where(Order.order_date >= self.parameters.dateStart if self.parameters.dateStart != None else None,
                        Order.order_date <= self.parameters.dateEnd if self.parameters.dateEnd != None else None,
                        Product.company == self.parameters.company))

        result = Results()
        revenue = sum(row.product_sale_price * row.quantity for row in query)
        result.result = revenue
        result.resultPerDate = []
        for row in query.dicts():
            result.resultPerDate.append(
                {'date': row.order_date, 'result': row.product_sale_price * row.quantity})

        self.dbConnection.close_connection()
        return result

    def Profits(self) -> Results:
        self.dbConnection.start_connection()
        query = (Order.select(Order.order_date, OrderProduct.quantity, Product.product_sale_price, Product.product_cost_price)
                 .join(OrderProduct)
                 .join(Product)
                 .where(Order.order_date >= self.parameters.dateStart if self.parameters.dateStart != None else None, Order.order_date <= self.parameters.dateEnd if self.parameters.dateEnd != None else None, Product.company == self.parameters.company
                        ))

        result = Results()
        profit = sum((row.product_sale_price - row.product_cost_price)
                     * row.quantity for row in query)
        result.result = profit
        result.resultPerDate = []
        for row in query.dicts():
            result.resultPerDate.append({'date': row.order_date, 'result': (
                row.product_sale_price - row.product_cost_price) * row.quantity})

        self.dbConnection.close_connection()
        return result

    def Orders(self) -> list:
        self.dbConnection.start_connection()
        query = (Order.select(fn.SUM(Order.order_id).alias("Amount"), Order.order_date)
                 .where(Order.order_date >= self.parameters.dateStart if self.parameters.dateStart != None else None,
                        Order.order_date <= self.parameters.dateEnd if self.parameters.dateEnd != None else None,
                        Product.company == self.parameters.company)
                 .group_by(Order.order_date)
                 .dicts())
        self.dbConnection.close_connection()
        return query

    def Categories(self) -> list:
        self.dbConnection.start_connection()
        query = (Order.select(fn.SUM(ProductCategory.primary_key).alias("Amount"), Category.name)
                 .join(OrderProduct, on=(OrderProduct.order == Order.order_id))
                 .join(ProductCategory, on=(OrderProduct.product == ProductCategory.product))
                 .join(Category, on=(ProductCategory.category == Category.category_id))
                 .join(Product, on=(OrderProduct.product == Product.product_id))
                 .where(Order.order_date >= self.parameters.dateStart if self.parameters.dateStart else None,
                        Order.order_date <= self.parameters.dateEnd if self.parameters.dateEnd else None,
                        Product.company == self.parameters.company)
                 .group_by(ProductCategory.category)
                 .dicts())

        self.dbConnection.close_connection()
        return query

    def OrderMethods(self) -> list:
        self.dbConnection.start_connection()
        query = (Order.select(fn.SUM(Order.order_id).alias("Amount"), OrderMethod.order_method_name)
                 .join(Product)
                 .join(OrderMethod, on=(Order.order_method == OrderMethod.order_method_id))
                 .where(Order.order_date >= self.parameters.dateStart if self.parameters.dateStart != None else None,
                        Order.order_date <= self.parameters.dateEnd if self.parameters.dateEnd != None else None,
                        Product.company == self.parameters.company)
                 .group_by(Order.order_method)
                 .dicts())
        self.dbConnection.close_connection()
        return query

    def Products(self) -> list:
        self.dbConnection.start_connection()
        query = (Order.select(fn.SUM(OrderProduct.quantity).alias("Amount"), Product.product_name)
                 .join(OrderProduct, on=(OrderProduct.order == Order.order_id))
                 .join(Product, on=(OrderProduct.product == Product.product_id))
                 .where(Order.order_date >= self.parameters.dateStart if self.parameters.dateStart != None else None,
                        Order.order_date <= self.parameters.dateEnd if self.parameters.dateEnd != None else None,
                        Product.company == self.parameters.company)
                 .group_by(OrderProduct.product)
                 .dicts())
        self.dbConnection.close_connection()
        return query

    def Countries(self) -> list:
        self.dbConnection.start_connection()
        query = (Order.select(fn.SUM(Order.order_id).alias("Amount"), Customer.country)
                 .join(Product)
                 .join(Customer, on=(Order.customer == Customer.customer_id))
                 .where(Order.order_date >= self.parameters.dateStart if self.parameters.dateStart != None else None,
                        Order.order_date <= self.parameters.dateEnd if self.parameters.dateEnd != None else None,
                        Product.company == self.parameters.company)
                 .group_by(Customer.country)
                 .dicts())
        self.dbConnection.close_connection()
        return query
