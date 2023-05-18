import peewee
import os


class Database:
    def __init__(self):
        self.db_path = os.getenv('DATABASE_PATH', 'database.db')
        self.db = peewee.SqliteDatabase(self.db_path)

    def getDatabaseConnection(self):
        return self.db

    def start_connection(self):
        self.db.connect()
        return self.db

    def close_connection(self):
        if not self.db.is_closed():
            self.db.close()
