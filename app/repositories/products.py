from abc import abstractmethod
from typing import Union, List

from app.models.products import Product
from app.repositories.abstractions import AbstractRepository


class ProductRepository(AbstractRepository):  # TODO ProductAbstractRepository

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
    def update(self, *args, **kwargs) -> Union[Product, None]:
        ...

    @abstractmethod
    def delete(self, *args, **kwargs) -> Union[Product, None]:
        ...
