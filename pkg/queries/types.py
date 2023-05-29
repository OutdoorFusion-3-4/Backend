from dataclasses import dataclass

class BaseQueryParameters:
    companies: list

    def __init__(self):
        self.companies = []


class GraphQueryParameters(BaseQueryParameters):
    dateStart: str
    dateEnd: str
    def __init__(self):
        self.dateStart = None
        self.dateEnd = None

@dataclass
class _ResultsPerDate:
    Amount: float
    Date: str

@dataclass
class Results:
    fields: list[str]
    resultPerDate: list[_ResultsPerDate]
    def __init__(self):
        self.fields = []
        self.resultPerDate = []
