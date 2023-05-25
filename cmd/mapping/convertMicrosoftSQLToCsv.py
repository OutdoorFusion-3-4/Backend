import sys
sys.path.append('./')

from core.mapping.MicrosoftSQLToCsv import export_tables_to_csv

def main():
    server = 'DESKTOP-1BENQ06\SQLEXPRESS'
    database = 'x'
    export_tables_to_csv(server, database)

if __name__ == '__main__':
    main()
