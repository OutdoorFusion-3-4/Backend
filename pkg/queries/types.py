class BaseQueryParameters:
    company: int


class GraphQueryParameters(BaseQueryParameters):
    dateStart: str
    dateEnd: str


class _ResultsPerDate:
    date: str
    result: float


class Results:
    result: float
    resultPerDate: _ResultsPerDate
