from abc import ABC, abstractmethod
from typing import Any


class DataSource(ABC):

    @abstractmethod
    def add(self, obj) -> None:
        pass

    @abstractmethod
    def find(self, _id: Any) -> None:
        pass

    @abstractmethod
    def list(self) -> None:
        pass
