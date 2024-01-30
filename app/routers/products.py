from typing import Union

from fastapi import APIRouter, HTTPException
from pydantic import PositiveInt, ValidationError

from app.databases.products import PRODUCTS_DB
from app.databases.users import USERS_DB
from app.models.products import ProductSearch

router = APIRouter(
    prefix="/products",
    tags=["products",]
)


@router.get("")
def list_products(
        keyword: str,
        category: Union[str, None] = None,
        limit: PositiveInt = 10
):
    try:
        ProductSearch(
            keyword=keyword,
            category=category,
            limit=limit,
        )

    except ValidationError as exc:
        detail = exc.errors()[0]
        raise HTTPException(status_code=422, detail=detail.get("msg"))

    result = []
    index = 0
    while len(result) < limit and index < len(PRODUCTS_DB):
        product = PRODUCTS_DB[index]

        if category:
            if product.get("category") != category:
                index += 1
                continue

        if keyword.lower() in product.get("name").lower():
            result.append(product)

        index += 1

    if not result:
        raise HTTPException(
            status_code=404,
            detail="There are no products with these parameters",
        )

    return result


@router.get("/{product_id}")
def get_product(product_id: PositiveInt):
    product = [
        item for item in PRODUCTS_DB if item.get("product_id") == product_id
    ]

    if not product:
        raise HTTPException(
            status_code=404,
            detail=f"There are no products with id '{product_id}'",
        )

    return product[0]
