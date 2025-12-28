from abc import ABC, abstractmethod

class BaseConnector(ABC):
    @abstractmethod
    def load(self, path: str):
        pass

    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def get_nodes(self):
        pass

    @abstractmethod
    def get_edges(self):
        pass
