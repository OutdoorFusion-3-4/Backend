import bcrypt
import csv


def register(username, password):
    with open("../../core/storage/users.csv", 'r') as readFile:
        reader = csv.reader(readFile, delimiter=' ')
        for row in reader:
            try:
                print(row[0].split(",")[0])
                if row[0].split(",")[0] == username:
                    print("Username already exists")
                    return False
            except:
                pass

        with open("../../core/storage/users.csv", 'a', newline='') as writeFile:
            writer = csv.writer(writeFile)
            salt = bcrypt.gensalt()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
            writer.writerow([username, hashed_password])

    return True


def Login(username, password):
    with open("../../core/storage/users.csv", 'r') as readFile:
        reader = csv.reader(readFile)
        for row in reader:
            if row[0] == username:
                password_bytes = password.encode('utf-8')
                hashed_password = row[1].encode('utf-8')[2:-1]
                check = bcrypt.checkpw(password_bytes, hashed_password)
                return check
