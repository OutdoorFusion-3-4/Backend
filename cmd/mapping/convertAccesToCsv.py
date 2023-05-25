import sys
sys.path.append('./')

from core.mapping.accesdbToCsv import transfer_access_to_csv

def main():
    DatabaseName = 'aenc.accdb'
    ProcessFolderName = 'verwerken'
    transfer_access_to_csv(DatabaseName, ProcessFolderName)

if __name__ == '__main__':
    main()
