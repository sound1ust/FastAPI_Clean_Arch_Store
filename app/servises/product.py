from typing import Union, List

from app.models.products import Product
from app.servises.abstract import AbstractService


class ProductService(AbstractService):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app_name = "PRODUCT"
        self.repo = self.get_repo()

    async def create(self, name, category, price) -> Union[Product, None]:
        stored_data = await self.repo.create(name, category, price)
        return self.get_product_object(stored_data)

    async def get(self, product_id) -> Union[Product, None]:
        stored_data = await self.repo.get(product_id)
        return self.get_product_object(stored_data)

    async def list(self, keyword, category, limit) -> Union[List[Product], None]:
        stored_data = await self.repo.list(keyword, category, limit)
        products = list(map(self.get_product_object, stored_data))
        return products

    async def update(self, product_id, name, category, price) -> Union[Product, None]:
        stored_data = await self.repo.update(product_id, name, category, price)
        return self.get_product_object(stored_data)

    async def delete(self, product_id) -> Union[Product, None]:
        stored_data = await self.repo.delete(product_id)
        return self.get_product_object(stored_data)

    @staticmethod
    def get_product_object(stored_data) -> Product:
        return Product(**{key: value for key, value in stored_data.items()})
