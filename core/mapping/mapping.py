from core.storage.dbModels import Company, Product, Category, ProductCategory, Customer, Order, OrderProduct, OrderMethod
import datetime
import logging

def get_mapped_column(table, original_column_name):
    column_names = table["column_names"]
    if original_column_name in column_names:
        return column_names[original_column_name]
    return None

def log_exception(table, e, row):
    logging.error(f"Error creating {table}: {e}")
    logging.error(f"Row data: {row}")

def create_company(table, row):
    company_name = get_mapped_column(table, "company_name")
    try:
        company, created = Company.get_or_create(company_name=company_name)
        return company
    except Exception as e:
        log_exception("Company",e, row)
    return None


def create_product(mapping, table, row):
    mapped_column_product_name = get_mapped_column(table, "product_name")
    mapped_column_product_sale_price = get_mapped_column(table, "product_sale_price")
    mapped_column_product_cost_price = get_mapped_column(table, "product_cost_price")
    mapped_column_product_description = get_mapped_column(table, "description")
    company_table = next((t for t in mapping['tables'] if t['table_name'] == 'Company'), None)
    mapped_column_product_company = get_mapped_column(company_table, "company_name") if company_table else None
    product_name = row[mapped_column_product_name] if row.get(mapped_column_product_name) else None
    product_sale_price = float(row[mapped_column_product_sale_price]) if row.get(mapped_column_product_sale_price) else None
    product_cost_price = float(row[mapped_column_product_cost_price]) if row.get(mapped_column_product_cost_price) else None
    product_description = row[mapped_column_product_description] if mapped_column_product_description and row.get(mapped_column_product_description) else None
    category_name = None
    try:
        product_company = Company.get(Company.company_name == mapped_column_product_company)
    except Company.DoesNotExist:
        print(f"Company '{mapped_column_product_company}' does not exist. Creating a new company.")
        product_company = Company.create(company_name=mapped_column_product_company)
    if product_name is not None:
        original_product_id = row.get(get_mapped_column(table, "original_id"))
        if row.get(get_mapped_column(table, "category_id")) is not None and row.get(get_mapped_column(table, "category_id")) != '':
            original_category_id = int(float(row.get(get_mapped_column(table, "category_id"))))
        else:
            original_category_id = ''
        if (row.get(get_mapped_column(table, "category"))) is not None:
            category_name = row.get(get_mapped_column(table, "category"))
        try:
            product, created = Product.get_or_create(
                product_name=product_name,
                product_sale_price=product_sale_price,
                product_cost_price=product_cost_price,
                description=product_description,
                company=product_company)
            return product, original_product_id, original_category_id, category_name, None  # Return created product instance
        except Exception as e:
            log_exception("Product",e, row)
    return None, None, None, None, None


def single_create_product_category(product, categories):
    if product[0] is not None and categories is not\
            None:
        try:
            for category in categories:
                product_category, created = ProductCategory.get_or_create(
                    product=product[0],
                    category=category[0]
                )
        except Exception as e:
            print(f"Error creating product category: {e}")

def create_category(table, row):
    mapped_column_name = get_mapped_column(table, "name")
    mapped_column_category = get_mapped_column(table, "category_id")
    mapped_column_other_category = get_mapped_column(table, "OtherCategory_id")
    other_category = row.get(mapped_column_other_category)
    original_id = row.get(mapped_column_category)
    if mapped_column_name in row:
        category_name = row[mapped_column_name]
        try:
            category, created = Category.get_or_create(name=category_name)
            return category, original_id, other_category, category_name
        except Exception as e:
            log_exception("Category",e, row)
    return None, None, None, None

def create_product_category(product, globalinstances):
    categorylist = []
    if product[0]:
        product_cat = ''
        cat_id = 0
        for product_instance in globalinstances.get('product', []):
            new_product_id, original_product_id, og_category_id, possible_category_name = product_instance
            if new_product_id == product[0]:
                cat_id = og_category_id
                product_cat = possible_category_name
        for category_instance in globalinstances.get('category', []):
            new_category_id, original_category_id, other_category_id, category_name = category_instance
            if original_category_id is not None:
                if int(original_category_id) == cat_id:
                    matched_category = new_category_id
                    categorylist.append(matched_category)
                    if other_category_id is not None:
                        categorylist.append(other_category_id)
            elif product_cat == category_name:
                categorylist.append(new_category_id)
        if product[0] is not None and categorylist is not None:
            try:
                for category in categorylist:
                    product_category, created = ProductCategory.get_or_create(
                        product=product[0],
                        category=category
                    )
            except Exception as e:
                print(f"Error creating product category: {e}")


def create_customer(table, row):
    mapped_column_name = get_mapped_column(table, "name")
    mapped_column_country = get_mapped_column(table, "country")
    mapped_column_birthday = get_mapped_column(table, "birthday")
    mapped_column_gender = get_mapped_column(table, "gender")

    name = ' '.join(row.get(name_part, '') for name_part in mapped_column_name) if isinstance(mapped_column_name, list) else row.get(mapped_column_name)
    country = row.get(mapped_column_country)
    gender = row.get(mapped_column_gender)

    if isinstance(mapped_column_birthday, list):
        day, month, year = (row.get(col) for col in mapped_column_birthday)
        birthday = f"{day}-{month}-{year}"
    else:
        birthday = row.get(mapped_column_birthday)

    if birthday:
        birthday = datetime.datetime.strptime(birthday, "%d-%B-%Y")

    if(name == ' ' or name == None):
        if not (country or birthday or gender):
            return None, None

    try:
        customer = Customer.create(
            name=name,
            country=country,
            birthday=birthday,
            gender=gender
        )
        original_customer_id = row.get(get_mapped_column(table, "customer_id"))
        return customer, original_customer_id
    except Exception as e:
        log_exception("Customer",e, row)

    return None, None

def create_order_method(table, row):
    mapped_column_order_method_name = row.get(get_mapped_column(table, "orderMethod_name"))
    mapped_column_order_method_Id = row.get(get_mapped_column(table, "orderMethod_id"))

    if mapped_column_order_method_name and mapped_column_order_method_Id:
        try:
            orderMethod = OrderMethod.create(
                order_method_name = mapped_column_order_method_name
            )
            return orderMethod, mapped_column_order_method_Id  # Return created order instance
        except Exception as e:
            log_exception("OrderMethod",e, row)
    return None, None
def create_order(table, row, customer, globalinstances):
    shipping_method = None
    mapped_column_order_date = get_mapped_column(table, "order_date")
    mapped_column_shipping_method = get_mapped_column(table, "shipping_method")

    customerId = row.get(get_mapped_column(table, "customer"))

    if isinstance(mapped_column_order_date, list):
        day, month, year = (row.get(col) for col in mapped_column_order_date)
        order_date = f"{day}-{month}-{year}"
    else:
        order_date = row.get(mapped_column_order_date)

    if not order_date or not customer:
        return None

    original_order_id = row.get(get_mapped_column(table, "original_id"))

    matched_customer = None
    for customer_tuple in globalinstances.get('customer', []):
        customer_instance, original_customer_id = customer_tuple
        if original_customer_id == customerId:
            matched_customer = customer_instance

            break

    if not matched_customer:
        matched_customer = customer[0]

    matched_ordermethod = None
    if row.get(get_mapped_column(table, "orderMethod_name")) != '':
        for orderMethod in globalinstances.get('ordermethod', []):
            new_ordermethod, old_ordermethod = orderMethod
            if row.get(mapped_column_shipping_method) == old_ordermethod:
                matched_ordermethod = new_ordermethod
    if order_date:
        try:
            order_date = datetime.datetime.strptime(order_date, "%Y-%m-%d")
        except ValueError:
            try:
                order_date = datetime.datetime.strptime(order_date, "%d-%b-%Y %I:%M:%S %p")
            except ValueError:
                print(
                    "The date format is not recognized. Please use either 'YYYY-MM-DD' or 'DD-Mon-YYYY hh:mm:ss AM/PM'.")
                order_date = None

    if order_date:
        order_date = order_date.strftime('%Y-%m-%d')

    try:
        order = Order.create(
            order_date=order_date,
            customer=matched_customer,
            order_method_id=matched_ordermethod
        )
        return order, original_order_id  # Return created order instance
    except Exception as e:
        log_exception("Order",e, row)

    return None, None


def create_order_product(table, row, order, product, globalinstances):
    order_id = row.get(get_mapped_column(table, "order_id"))
    product_id = row.get(get_mapped_column(table, "product_id"))
    matched_order = None
    matched_product = None

    if globalinstances.get('product') and globalinstances.get('order') is not None and globalinstances.get('order')[0][1] is not None:
        for order_instance in globalinstances.get('order', []):
            new_order_id, original_order_id = order_instance
            if original_order_id == order_id:
                matched_order = new_order_id
                break

        for product_instance in globalinstances.get('product', []):
            new_product_id, original_product_id, original_category_id = product_instance
            if original_product_id == product_id:
                matched_product = new_product_id
                break

    if not matched_order or not matched_product:
        matched_order = order[0]
        matched_product = product[0]

    mapped_column_quantity = get_mapped_column(table, "quantity")
    if row.get(mapped_column_quantity) and matched_product and matched_order:
        quantity = int(row[mapped_column_quantity])
        order_product = OrderProduct.create(
            quantity=quantity,
            order=matched_order,
            product=matched_product
        )
        return order_product
    else:
        return None



def create_order_product_multiple(table, row, globalinstances):
    order_id = row.get(get_mapped_column(table, "order_id"))
    product_id = row.get(get_mapped_column(table, "product_id"))
    matched_order = None
    matched_product = None

    if globalinstances.get('product') and globalinstances.get('order')[0][1] is not None:
        for order_instance in globalinstances.get('order', []):
            new_order_id, original_order_id = order_instance
            if original_order_id == order_id:
                matched_order = new_order_id
                break

        for product_instance in globalinstances.get('product', []):
            new_product_id, original_product_id, original_category_id, possible_category_name = product_instance
            if original_product_id == product_id:
                matched_product = new_product_id
                break
    if not matched_order or not matched_product:
        return

    mapped_column_quantity = get_mapped_column(table, "quantity")
    if row.get(mapped_column_quantity) and matched_product and matched_order:
        quantity = int(row[mapped_column_quantity])

        order_product = OrderProduct.create(
            quantity=quantity,
            order=matched_order,
            product=matched_product
        )
        return order_product
    else:
        return None




