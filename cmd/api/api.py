import sys
sys.path.append('./')
import os 
os.environ['db'] = 'database.db'
import pkg.server.server as server

def main():
    server.run()

if __name__ == '__main__':
    main()
