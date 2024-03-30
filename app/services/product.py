from typing import Union, List

from pydantic import PositiveInt, PositiveFloat

from app.models.products import Product
from app.services.abstract import AbstractService


class ProductService(AbstractService):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.app_name = "PRODUCT"
        self.repo = self.get_repo()

    async def create(
            self,
            name: str,
            category: str,
            price: PositiveFloat,
    ) -> Union[Product, None]:
        product = await self.repo.create(name, category, price)
        return product

    async def get(
            self,
            product_id: PositiveInt,
    ) -> Union[Product, None]:
        product = await self.repo.get(product_id)
        return product

    async def list(
            self,
            keyword: str = "",
            category: Union[str, None] = None,
            limit: PositiveInt = 10,
    ) -> Union[List[Product], None]:
        list_products = await self.repo.list(keyword, category, limit)
        return list_products

    async def update(
            self,
            product_id: PositiveInt,
            name: str,
            category: str,
            price: PositiveFloat,
    ) -> Union[Product, None]:
        product = await self.repo.update(product_id, name, category, price)
        return product

    async def delete(
            self,
            product_id: PositiveInt,
    ) -> Union[Product, None]:
        product = await self.repo.delete(product_id)
        return product
