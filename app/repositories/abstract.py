from abc import abstractmethod, ABC
from typing import List

from app.models.products import Product


class AbstractRepository(ABC):
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def create(self, *args, **kwargs) -> Product:
        ...

    @abstractmethod
    def get(self, *args, **kwargs) -> Product:
        ...

    @abstractmethod
    def list(self, *args, **kwargs) -> List[Product]:
        ...

    @abstractmethod
    def update(self, *args, **kwargs) -> Product:
        ...

    @abstractmethod
    def delete(self, *args, **kwargs) -> Product:
        ...
