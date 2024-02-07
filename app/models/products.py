from pydantic import BaseModel, PositiveInt, PositiveFloat, constr
from typing import Union


class Product(BaseModel):
    product_id: PositiveInt
    name: constr(min_length=3, max_length=50)
    category: constr(min_length=3, max_length=50)
    price: PositiveFloat


class ProductCreate(BaseModel):
    name: constr(min_length=3, max_length=50)
    category: constr(min_length=3, max_length=50)
    price: PositiveFloat


class ProductSearch(BaseModel):
    keyword: constr(min_length=0, max_length=50) = ""
    category: Union[str, None] = None
    limit: PositiveInt = 10
