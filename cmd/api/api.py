import sys
sys.path.append('./')
import pkg.api.server as server

def main():
    s = server.Server()
    s.run()

if __name__ == '__main__':
    main()
