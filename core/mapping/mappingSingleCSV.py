import csv
from core.mapping.mapping import *
import peewee
from pkg.queries.baseQueries import *
class mappingSingleCsv (BaseQueries):
    def __init__(self, dbConnection: IDatabase):
        self.dbConnection = dbConnection
    def process_single_csv(self, filename, mapping, globalinstances):
        customer_mapping = {}
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                instances = {}
                with self.dbConnection.atomic():
                    for table in mapping['tables']:
                        if table['table_name'] == 'Company':
                            instances.setdefault('company', []).append(create_company(table, row))
                        elif table['table_name'] == 'Product':
                            product, original_product_id, original_category_id, category_name, subcategory_name = create_product(mapping, table, row)  # Pass globalinstances as an argument
                            instances.setdefault('product', []).append(product)
                            if product:
                                globalinstances.setdefault('product', []).append((product, original_product_id))
                        elif table['table_name'] == 'Category':
                            instances.setdefault('category', []).append(create_category(table, row))
                        elif table['table_name'] == 'Customer':
                            customer, original_customer_id = create_customer(table, row)
                            if customer and original_customer_id:
                                # Store the mapping in the dictionary
                                customer_mapping[original_customer_id] = customer.id
                                globalinstances.setdefault('customer', []).append((customer, original_customer_id))
                            instances.setdefault('customer', []).append(customer)
                        elif table['table_name'] == 'Order':
                            order, original_order_id = create_order(table, row, instances.get('customer', None), globalinstances) or (None, None)
                            instances.setdefault('order', []).append(order)
                            if order:
                                globalinstances.setdefault('order', []).append((order, original_order_id))

                    if 'product' in instances and 'category' in instances and instances['product'] and instances['category']:
                        single_create_product_category(instances['product'], instances['category'])

                    if 'order' in instances and 'product' in instances and instances['order'] and instances['product']:
                        create_order_product(table, row, instances['order'], instances['product'], globalinstances)
