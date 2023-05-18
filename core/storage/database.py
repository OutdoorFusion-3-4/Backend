from abc import ABC, abstractmethod

class IDatabase(ABC):
    @abstractmethod
    def getDatabaseConnection(self):
        pass
    @abstractmethod
    def start_connection(self):
        pass
    @abstractmethod
    def close_connection(self):
        pass