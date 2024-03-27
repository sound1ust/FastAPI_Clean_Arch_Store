from abc import abstractmethod, ABC
from typing import List

from asyncpg import Record


class AbstractRepository(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def create(self, *args, **kwargs) -> Record:
        ...

    @abstractmethod
    def get(self, *args, **kwargs) -> Record:
        ...

    @abstractmethod
    def list(self, *args, **kwargs) -> List[Record]:
        ...

    @abstractmethod
    def update(self, *args, **kwargs) -> Record:
        ...

    @abstractmethod
    def delete(self, *args, **kwargs) -> Record:
        ...
