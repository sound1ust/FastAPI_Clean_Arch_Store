from pydantic import BaseModel, PositiveInt, field_validator
from typing import Union

from app.databases.products import PRODUCTS_DB


class Product(BaseModel):
    product_id: PositiveInt
    name: str
    category: str
    price: float


class ProductSearch(BaseModel):
    keyword: str
    category: Union[str, None] = None
    limit: PositiveInt = 10

    @field_validator("category")
    def validate_category(cls, category):
        if not category:
            return

        if category not in set(item.get("category") for item in PRODUCTS_DB):
            raise ValueError(
                f"There is no category '{category}' in the products"
            )
