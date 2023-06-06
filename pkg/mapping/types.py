from dataclasses import dataclass

@dataclass 
class MappingTable:
    table_name: str
    columnTableName: str
    column_names: list[str]
    def __init__(self):
        self.table_name = None
        self.columnTableName = None
        self.column_names = []


@dataclass
class MappingData:
    tables: list[MappingTable]
    def __init__(self):
        self.tables = []
