import peewee

class Database:
    def __init__(self, db_path):
        self.db_path = db_path
        self.db = peewee.SqliteDatabase(self.db_path)

    def start_connection(self):
        self.db.connect()
        return self.db

    def close_connection(self):
        if not self.db.is_closed():
            self.db.close()
