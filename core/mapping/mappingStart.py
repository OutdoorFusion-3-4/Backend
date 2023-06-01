import sys
sys.path.append('./')
import json
import os
import peewee
import chardet
from core.mapping.mappingSingleCSV import *
csv.field_size_limit(2147483647)
from pkg.queries.baseQueries import *
class mapping (BaseQueries):
    def __init__(self, dbConnection: IDatabase):
        self.dbConnection = dbConnection
    def get_file_encoding(self, file_path):
        with open(file_path, 'rb') as file:
            result = chardet.detect(file.read())
        return result['encoding']

    def process_csv_folder(self, folder_name, mapping_file):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_file = os.path.join(current_dir, mapping_file)
        folder_path = os.path.join(current_dir, folder_name)
        with open(json_file, 'r') as mapping_file:
            mapping = json.load(mapping_file)

        globalinstances = {}

        csv_count = sum(1 for filename in os.listdir(folder_path) if filename.endswith('.csv'))

        if csv_count < 2:
            self.process_all_files_in_folder(folder_path, self.process_single_csv, mapping, globalinstances)
        else:
            self.process_all_files_in_folder(folder_path, self.first_process_csv, mapping, globalinstances)
            self.process_all_files_in_folder(folder_path, self.second_process_csv, mapping, globalinstances)
            self.process_all_files_in_folder(folder_path, self.third_process_csv, mapping, globalinstances)
    def process_all_files_in_folder(self,folder_path, processing_function, mapping, globalinstances):
        for filename in os.listdir(folder_path):
            self.process_csv_file(filename, folder_path, processing_function, mapping, globalinstances)
    def process_csv_file(self, filename, folder_path, processing_function, mapping, globalinstances):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            processing_function(file_path, mapping, globalinstances)

    def first_process_csv(self, filename, mapping, globalinstances):
        with open(filename, 'r', encoding=self.get_file_encoding(filename)) as file:
            reader = csv.DictReader(file)
            for row in reader:
                condition_met = False
                with self.dbConnection.atomic():
                    for table in mapping['tables']:
                        if table['table_name'] == 'OrderMethod':
                            ordermethod, original_ordermethod_id= create_order_method(table, row)

                            if ordermethod:
                                globalinstances.setdefault('ordermethod', []).append((ordermethod, original_ordermethod_id))
                                condition_met = True
                        elif table['table_name'] == 'Product':
                            if (('custom_table_name' not in table) or ('custom_table_name' in table and os.path.basename(filename) == table['custom_table_name'])):
                                product, original_product_id, og_category_id, possible_category_name, possible_subcategory_name = create_product(mapping, table, row)  # Pass globalinstances as an argument
                                if product:
                                    globalinstances.setdefault('product', []).append((product, original_product_id, og_category_id, possible_category_name))
                                condition_met = True
                        elif table['table_name'] == 'Customer':
                            customer, original_customer_id = create_customer(table, row)
                            if customer and original_customer_id:
                                globalinstances.setdefault('customer', []).append((customer, original_customer_id))
                            condition_met = True
                if not condition_met:
                    return
    def second_process_csv(self, filename, mapping, globalinstances):
        with open(filename, 'r', encoding=self.get_file_encoding(filename)) as file:
            reader = csv.DictReader(file)
            for row in reader:
                condition_met = False
                with self.dbConnection.atomic():
                    for table in mapping['tables']:
                        if table['table_name'] == 'Company':
                            condition_met = True
                        elif table['table_name'] == 'Category':
                            if (('custom_table_name' not in table) or ('custom_table_name' in table and os.path.basename(filename) == table['custom_table_name'])):
                                category, original_category_id, other_category, category_name = create_category(table, row)
                                if category:
                                    globalinstances.setdefault('category', []).append((category, original_category_id, other_category, category_name))
                                condition_met = True
                        elif table['table_name'] == 'Order':
                            if (('custom_table_name' not in table) or ('custom_table_name' in table and os.path.basename(filename) == table['custom_table_name'])):
                                order, original_order_id = create_order(table, row, globalinstances.get('customer'), globalinstances) or (None, None)
                                if order:
                                    globalinstances.setdefault('order', []).append((order, original_order_id))
                                condition_met = True
                if not condition_met:
                    return


    def third_process_csv(self, filename, mapping, globalinstances):
        products = globalinstances.get('product', [])
        if products:
            for product in products:
                create_product_category(product, globalinstances)

        with open(filename, 'r', encoding=self.get_file_encoding(filename)) as file:
            reader = csv.DictReader(file)
            for row in reader:
                i = 0
                condition_met = False
                for table in mapping['tables']:
                    if table['table_name'] == 'OrderProduct':
                        columns = table['column_names']
                        custom_table_name = table.get('custom_table_name')
                        file_name_check = custom_table_name and os.path.basename(filename) == custom_table_name
                        if 'order_id' in columns and 'product_id' in columns and (not custom_table_name or file_name_check):
                            condition_met = True
                            create_order_product_multiple(table, row, globalinstances)
                            break
                        else:
                            orders = globalinstances.get('order', [[None, None]])[0][1]
                            products = globalinstances.get('product', [])
                            if not orders:
                                create_order_product(table, row, orders[i], products[i], globalinstances)
                                i += 1
                                condition_met = True
                if not condition_met:
                    return




