from pkg.storage.database import IDatabase
from dateutil import parser
class BaseQueries:
    def __init__(self, dbConnection: IDatabase):
        self.dbConnection = dbConnection

    def from_iso_string(self, iso_string: str):
        # Check if iso string is None
        if iso_string is None or iso_string == '':
            return None

        # Convert ISO string to datetime object
        dt = parser.isoparse(iso_string)
        return dt
