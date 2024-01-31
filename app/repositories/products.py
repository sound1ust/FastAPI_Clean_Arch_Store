from abc import ABC, abstractmethod

from pydantic import PositiveInt

from app.models.products import ProductSearch


class ProductRepository(ABC):
    @abstractmethod
    def create_product(self, data: dict):
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
