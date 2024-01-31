from pydantic import BaseModel, PositiveInt, field_validator, PositiveFloat
from typing import Union

from app.databases.products import PRODUCTS_DB


class Product(BaseModel):
    product_id: PositiveInt
    name: str
    category: str
    price: PositiveFloat


class ProductCreate(BaseModel):
    name: str
    category: str
    price: PositiveFloat

    @field_validator("name")
    def validate_name(cls, name):
        if len(name) < 3:
            raise ValueError(
                f"Too short name: the length of {name} < 3 symbols."
            )
        return name

    @field_validator("category")
    def validate_category(cls, category):
        if len(category) < 3:
            raise ValueError(
                f"Too short category name: "
                f"the length of {category} < 3 symbols."
            )

        return category

    @field_validator("price")
    def validate_price(cls, price):
        if price <= 0:
            raise ValueError(
                f"Price must be higher than 0: {price}"
            )

        return price


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
