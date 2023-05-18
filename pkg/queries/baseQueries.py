import datetime
from pkg.storage.database import Database


class BaseQueries:
    def __init__(self, dbConnection: Database):
        self.dbConnection = dbConnection

    def from_iso_string(self, iso_string: str):
        # Check if iso string is None
        if iso_string is None or iso_string == '':
            return None

        # Convert ISO string to datetime object
        dt = datetime.datetime.fromisoformat(iso_string)
        return dt
