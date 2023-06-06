import sys
sys.path.append('./')
from pkg.auth.authentication import register
def main():
    register(username='a@a.com', password='password')

if __name__ == '__main__':
    main()