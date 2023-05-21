from core.storage.database import IDatabase
from core.storage.dbModels import Category, OrderMethod, Product, Order, OrderProduct, ProductCategory, Customer
from .types import GraphQueryParameters, Results
from .baseQueries import BaseQueries
from peewee import fn
from json import loads

class DataQueries (BaseQueries):
    def __init__(self, dbConnection: IDatabase, parameters: GraphQueryParameters):
        self.dbConnection = dbConnection
        self.parameters = parameters
        # transform string to list
        if type(self.parameters.companies) is str:
            self.parameters.companies = loads(self.parameters.companies)
        # transform iso string to datetime object
        self.parameters.dateStart = self.from_iso_string(
            self.parameters.dateStart)
        self.parameters.dateEnd = self.from_iso_string(self.parameters.dateEnd)

    def __checkDates(self, query: any, dateField: any) -> any:
        if self.parameters.dateStart is not None:
            query = query.where(dateField >= self.parameters.dateStart)

        if self.parameters.dateEnd is not None:
            query = query.where(dateField <= self.parameters.dateEnd)

        return query

    def __checkCompanies(self, query: any, companyField: any) -> any:
        if self.parameters.companies is None or len(self.parameters.companies) == 0:
            return query

        if len(self.parameters.companies) == 1:
            for company in self.parameters.companies:
                query = query.where(companyField == company)
            return query

        query = query.where(companyField.in_(self.parameters.companies))
        return query

    def Revenues(self) -> Results:
        self.dbConnection.start_connection()
        result = Results()
        query = (Order.select()
                 .join(OrderProduct)
                 .join(Product))
        query = self.__checkDates(query, Order.order_date)
        query = self.__checkCompanies(query, Product.company)
        query = query.distinct()
        for order in query:
            print(order)
        for order in query:
            orderProductQuery = (OrderProduct.select()
                                 .join(Product)
                                 .where(OrderProduct.order == order))

            result.result += sum(row.product.product_sale_price *
                                 row.quantity for row in orderProductQuery)
            for row in orderProductQuery:
                result.resultPerDate.append(
                    {'date': order.order_date, 'result': row.product.product_sale_price * row.quantity})

        self.dbConnection.close_connection()
        return result

    def Profits(self) -> Results:
        self.dbConnection.start_connection()
        result = Results()
        query = (Order.select()
                 .join(OrderProduct)
                 .join(Product))
        query = self.__checkDates(query, Order.order_date)
        query = self.__checkCompanies(query, Product.company)
        query = query.distinct()

        for order in query:
            orderProductQuery = (OrderProduct.select()
                                 .join(Product)
                                 .where(OrderProduct.order == order))

            result.result += sum((row.product.product_sale_price - row.product.product_cost_price) *
                                 row.quantity for row in orderProductQuery)
            for row in orderProductQuery:
                result.resultPerDate.append(
                    {'date': order.order_date, 'result': (row.product.product_sale_price - row.product.product_cost_price) * row.quantity})

        self.dbConnection.close_connection()
        return result

    def Orders(self) -> list:
        self.dbConnection.start_connection()
        query = (Order.select(fn.SUM(Order.order_id).alias("Amount"), Order.order_date)
                 .join(OrderProduct, on=(OrderProduct.order == Order.order_id))
                 .join(Product, on=(OrderProduct.product == Product.product_id)))

        query = self.__checkCompanies(query, OrderProduct.product.company)
        query = self.__checkDates(query, Order.order_date)
        self.dbConnection.close_connection()

        return list(query.dicts())

    def Categories(self) -> list:
        self.dbConnection.start_connection()
        
        query = (Category
                .select(Category.name, fn.SUM(OrderProduct.quantity).alias("Amount"))
                .join(ProductCategory)
                .join(Product)
                .join(OrderProduct))
        query = self.__checkDates(query, Order.order_date)
        query = self.__checkCompanies(query, Product.company)
        query = query.distinct()
        query = (query .group_by(Category.name))

        self.dbConnection.close_connection()
        return list(query.dicts())

    def OrderMethods(self) -> list:
        self.dbConnection.start_connection()
        query = (Order.select(fn.SUM(Order.order_id).alias("Amount"), OrderMethod.order_method_name)
                 .join(OrderProduct, on=(OrderProduct.order == Order.order_id))
                 .join(Product)
                 .join(OrderMethod, on=(Order.order_method == OrderMethod.order_method_id)))
        query = self.__checkDates(query, Order.order_date)
        query = self.__checkCompanies(query, Product.company)
        query = query.group_by(OrderMethod.order_method_name)
        self.dbConnection.close_connection()
        return list(query.dicts())

    def Products(self) -> list:
        self.dbConnection.start_connection()
        query = (Order.select(fn.SUM(OrderProduct.quantity).alias("Amount"), Product.product_name)
                 .join(OrderProduct, on=(OrderProduct.order == Order.order_id))
                 .join(Product, on=(OrderProduct.product == Product.product_id)))
        query = self.__checkDates(query, Order.order_date)
        query = self.__checkCompanies(query, Product.company)
        query = query.group_by(Product.product_name)

        self.dbConnection.close_connection()
        return list(query.dicts())

    def Countries(self) -> list:
        self.dbConnection.start_connection()
        query = (Order.select(Customer.country, fn.COUNT(Order.order_id).alias("Amount"))
                    .join(Customer, on=(Order.customer == Customer.customer_id))
                    .join(OrderProduct, on=(OrderProduct.order == Order.order_id))
                    .join(Product))
        query = self.__checkDates(query, Order.order_date)
        query = self.__checkCompanies(query, Product.company)
        query = query.group_by(Customer.country)
        query = query.distinct()
        self.dbConnection.close_connection()
        return list(query.dicts())
