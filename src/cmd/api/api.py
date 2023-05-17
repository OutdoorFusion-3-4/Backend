import bcrypt
import csv


def signUp():
    username = input("Nieuwe gebruikersnaam: ")
    password = input("Nieuw wachtwoord: ")
    with open("./users.csv", 'r') as readFile:
        reader = csv.reader(readFile, delimiter=' ')
        for row in reader:
            try:
                print(row)
                if row[0] == username:
                    print("Username already exists")
                    return 0
            except:
                pass

        with open("./users.csv", 'a', newline='') as writeFile:
            writer = csv.writer(writeFile)
            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(password.encode('utf-8'), salt)
            writer.writerow([username, hash])


def signIn():
    username = input("gebruikersnaam: ")
    with open("./users.csv", 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            if row[0] == username:
                password = input("password: ")
                bytes = password.encode('utf-8')
                hash = row[1].encode('utf-8')[2:-1]
                check = bcrypt.checkpw(bytes, hash)
                return check


def main():

    # ff om te testen zonder api
    option = input("Optie: \n1. singUp \n2. signIn\n")
    if option == "1":
        signUp()
    if option == "2":
        print(signIn())
    if option != 1 or option != 2:
        print("geen geldige optie probeer opnieuw")
        main()


if __name__ == "__main__":
    main()
