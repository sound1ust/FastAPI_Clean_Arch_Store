from abc import ABC, abstractmethod

from pydantic import PositiveInt
import asyncpg

from app.models.products import ProductSearch


class ProductRepository(ABC):
    def __init__(self, conn: asyncpg.Connection):
        self.conn = conn

    @abstractmethod
    def create_product(self, product_data: dict):
        ...

    @abstractmethod
    def get_product_by_id(self, product_id: PositiveInt):
        ...

    @abstractmethod
    def get_products_list(self, data: ProductSearch):
        ...

    @abstractmethod
    def delete_product(self, product_id: PositiveInt):
        ...
