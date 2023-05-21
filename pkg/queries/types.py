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


class _ResultsPerDate:
    date: str
    result: float


class Results:
    result: float
    resultPerDate: list[_ResultsPerDate]
    def __init__(self):
        self.result = 0
        self.resultPerDate = []
