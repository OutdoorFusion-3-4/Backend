import sys
sys.path.append('./')
import os
os.environ['db'] = 'database.db'
from pkg.storage.database import Database

from pkg.mapping.mappingStart import Mapping
def main():
    database = Database()
    m = Mapping(database)

    FileName = 'Northwind.json'
    ProcessFolderName = 'verwerken'
    print(m)
    m.process_csv_folder(ProcessFolderName, FileName)

if __name__ == '__main__':
    main()
