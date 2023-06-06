import csv
import os
import pyodbc

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

    folder_path = os.path.join(script_dir, folder_path)  # Update folder_path

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
