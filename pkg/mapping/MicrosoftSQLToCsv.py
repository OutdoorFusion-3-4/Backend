import pyodbc
import pandas as pd
import os
import warnings

def export_tables_to_csv(server, database):
    # Suppress warnings
    warnings.filterwarnings('ignore')

    # Set up your connection details

    driver = '{SQL Server}' # this might change depending on your SQL Server driver

    dbConnection = pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';Trusted_Connection=yes')

    cursor = dbConnection.cursor()

    # Get the list of user-defined table names
    table_names = cursor.execute("SELECT TABLE_SCHEMA, TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE'").fetchall()


    # Specify the folder name where you want to save the CSV files
    folder_name = "verwerken"

    # Get the directory of the current python script
    current_directory = os.path.dirname(os.path.realpath(__file__))

    # Create the new folder path
    folder_path = os.path.join(current_directory, folder_name)

    # Check if the folder does not exist, then create it
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Loop over the table names, read to DataFrame and write to .csv in the specified folder
    for table in table_names:
        schema_name = table[0]
        table_name = table[1]
        query = f"SELECT * FROM [{schema_name}].[{table_name}]"  # use f-string and add square brackets around the table name
        df = pd.read_sql(query, dbConnection)
        df.to_csv(os.path.join(folder_path, f'{table_name}.csv'), index=False)

    cursor.close()
    dbConnection.close()
