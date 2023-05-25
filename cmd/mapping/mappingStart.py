import sys
sys.path.append('./')
import os
os.environ['db'] = 'database.db'

from core.mapping.mappingStart import process_csv_folder
def main():

    FileName = 'BikeStoreSales.json'
    ProcessFolderName = 'verwerken'
    process_csv_folder(ProcessFolderName, FileName)

if __name__ == '__main__':
    main()
