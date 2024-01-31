from typing import Union

from fastapi import APIRouter, HTTPException
from pydantic import PositiveInt, ValidationError

from app.models.products import ProductSearch, Product, ProductCreate
from app.servises.products import ProductService

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
    data = {
        "keyword": keyword,
        "category": category,
        "limit": limit,
    }
    try:
        ProductSearch(**data)

    except ValidationError as exc:
        detail = exc.errors()[0]
        raise HTTPException(status_code=422, detail=detail.get("msg"))

    product_service = ProductService()

    products = product_service.get_products_list(data)

    if not products:
        raise HTTPException(
            status_code=404,
            detail="There are no products with these parameters",
        )

    return products


@router.get("/{product_id}")
def get_product(product_id: PositiveInt):
    product_service = ProductService()
    product = product_service.get_product_by_id(product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail=f"There are no products with id '{product_id}'",
        )

    return product


@router.post("", response_model=Product)
def create_product(data: ProductCreate):
    product_service = ProductService()

    try:
        product = product_service.create_product(data)

    except ValidationError as exc:
        detail = exc.errors()[0]
        raise HTTPException(status_code=422, detail=detail.get("msg"))

    return product


@router.delete("/{product_id}")
def delete_product(product_id: PositiveInt):
    product_service = ProductService()
    if product_service.delete_product(product_id):
        return {"detail": "Product deleted"}

    return HTTPException(status_code=404, detail="Product not found")

