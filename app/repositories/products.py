from abc import ABC, abstractmethod
from typing import Union, List

import asyncpg

from app.models.products import Product


class ProductRepository(ABC):  # ProductAbstractRepository
    def __init__(self, conn: asyncpg.Connection):  # AbstractConnection
        self.conn = conn

    @abstractmethod
    def create(self, *args, **kwargs) -> Union[Product, None]:
        ...

    @abstractmethod
    def get(self, *args, **kwargs) -> Union[Product, None]:
        ...

    @abstractmethod
    def list(self, *args, **kwargs) -> Union[List[Product], None]:
        ...

    @abstractmethod
    def delete(self, *args, **kwargs) -> Union[Product, None]:
        ...
