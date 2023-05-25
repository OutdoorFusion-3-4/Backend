import pyodbc

from core.mapping.mapping import *
import json
import os
import sys
import peewee
import chardet
csv.field_size_limit(2147483647)

from core.storage.database import IDatabase
db = peewee.SqliteDatabase('database.db')

def get_file_encoding(file_path):
    # rawdata is a bytes object
    with open(file_path, 'rb') as file:
        result = chardet.detect(file.read())
    return result['encoding']



def process_single_csv(filename, mapping, globalinstances):
    customer_mapping = {}
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            instances = {}
            with db.atomic():
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





def process_csv_folder(folder_name, mapping_file):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_file = os.path.join(current_dir, mapping_file)
    folder_path = os.path.join(current_dir, folder_name)

    with open(json_file, 'r') as mapping_file:
        mapping = json.load(mapping_file)

    globalinstances = {}  # Create a new globalinstances dictionary

    csv_count = 0  # Initialize a counter for CSV files

    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            csv_count += 1  # Increment the counter

    if csv_count < 2:
        for filename in os.listdir(folder_path):
            if filename.endswith('.csv'):
                file_path = os.path.join(folder_path, filename)
                process_single_csv(file_path, mapping, globalinstances)  # Pass the globalinstances dictionary
                return

    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            first_process_csv(file_path, mapping, globalinstances)  # Pass the globalinstances dictionary

    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            process_csv(file_path, mapping, globalinstances)  # Pass the globalinstances dictionary

    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            file_path = os.path.join(folder_path, filename)
            koppel_tables(file_path, mapping, globalinstances)  # Pass the globalinstances dictionary


def first_process_csv(filename, mapping, globalinstances):
    with open(filename, 'r', encoding=get_file_encoding(filename)) as file:
        reader = csv.DictReader(file)
        for row in reader:
            condition_met = False
            with db.atomic():
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
            if not condition_met:
                return
def process_csv(filename, mapping, globalinstances):
    customer_mapping = {}
    with open(filename, 'r', encoding=get_file_encoding(filename)) as file:
        reader = csv.DictReader(file)
        for row in reader:
            instances = {}
            condition_met = False
            with db.atomic():
                for table in mapping['tables']:
                    if table['table_name'] == 'Company':
                        instances.setdefault('company', []).append(create_company(table, row))
                        condition_met = True
                    elif table['table_name'] == 'Category':
                        if (('custom_table_name' not in table) or ('custom_table_name' in table and os.path.basename(filename) == table['custom_table_name'])):
                            category, original_category_id, other_category, category_name = create_category(table, row)
                            instances.setdefault('category', []).append(category)
                            if category:
                                globalinstances.setdefault('category', []).append((category, original_category_id, other_category, category_name))
                            condition_met = True
                    elif table['table_name'] == 'Customer':
                        customer, original_customer_id = create_customer(table, row)
                        if customer and original_customer_id:
                            # Store the mapping in the dictionary
                            customer_mapping[original_customer_id] = customer.id
                            globalinstances.setdefault('customer', []).append((customer, original_customer_id))
                        instances.setdefault('customer', []).append(customer)
                        condition_met = True
                    elif table['table_name'] == 'Order':
                        if (('custom_table_name' not in table) or ('custom_table_name' in table and os.path.basename(filename) == table['custom_table_name'])):
                            order, original_order_id = create_order(table, row, instances.get('customer', None), globalinstances) or (None, None)
                            instances.setdefault('order', []).append(order)
                            if order:
                                globalinstances.setdefault('order', []).append((order, original_order_id))
                            condition_met = True
            if not condition_met:
                return

def koppel_tables(filename, mapping, globalinstances):
    if globalinstances.get('product') is not None:
        for product in globalinstances.get('product'):
            create_product_category(product, globalinstances)
    with open(filename, 'r', encoding=get_file_encoding(filename)) as file:
        reader = csv.DictReader(file)
        for row in reader:
            i = 0
            condition_met = False
            for table in mapping['tables']:
                if table['table_name'] == 'OrderProduct':
                        if 'order_id' in table['column_names'] and 'product_id' in table['column_names'] and ('custom_table_name' not in table) or ('custom_table_name' in table and os.path.basename(filename) == table['custom_table_name']):
                            condition_met = True
                            create_order_product_multiple(table, row, globalinstances)
                            break  # If the condition is met, no need to check further tables
                        elif globalinstances.get('order',[])[0][1] is None:
                                create_order_product(table, row, globalinstances.get('order', [])[i], globalinstances.get('product', [])[i], globalinstances)
                                i=i+1
                                condition_met = True
            if not condition_met:
                return




def transfer_access_to_csv(database_filename, folder_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    database_path = os.path.join(script_dir, database_filename)

    conn_str = f'DRIVER={{Microsoft Access Driver (*.mdb, *.accdb)}};DBQ={database_path};'
    conn = pyodbc.connect(conn_str)

    cursor = conn.cursor()

    table_names = []
    for row in cursor.tables():
        if row.table_type == 'TABLE':
            table_names.append(row.table_name)

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    for table_name in table_names:
        query = f'SELECT * FROM [{table_name}]'
        cursor.execute(query)

        rows = cursor.fetchall()

        column_names = [column[0] for column in cursor.description]
        csv_filename = os.path.join(folder_path, f'{table_name}.csv')
        with open(csv_filename, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(column_names)
            writer.writerows(rows)
        print(f"Data transferred from table '{table_name}' to {csv_filename} successfully.")
    cursor.close()
    conn.close()




# Usage example
# transfer_access_to_csv('aenc.accdb', 'verwerken')


