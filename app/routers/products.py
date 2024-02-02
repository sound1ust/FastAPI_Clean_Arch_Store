from typing import Union

from fastapi import APIRouter, HTTPException, Depends
from pydantic import PositiveInt, ValidationError

from app.dependencies.auth import UserAndRoleChecker
from app.models.products import ProductSearch, Product, ProductCreate
from app.models.users import UserRole
from app.servises.products import ProductService
from database.dependencies import get_conn

router = APIRouter(
    prefix="/products",
    tags=["products",],
)


@router.get("")
async def list_products(
        keyword: str,
        category: Union[str, None] = None,
        limit: PositiveInt = 10,
        conn=Depends(get_conn),
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

    product_service = ProductService(conn)
    products = await product_service.get_products_list(data)

    if not products:
        raise HTTPException(
            status_code=404,
            detail="There are no products with these parameters",
        )

    return products


@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: PositiveInt, conn=Depends(get_conn)):
    product_service = ProductService(conn)
    product = await product_service.get_product_by_id(product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail=f"There are no products with id '{product_id}'",
        )

    return product


@router.post(
    "",
    response_model=Product,
    dependencies=[Depends(UserAndRoleChecker(UserRole.MODERATOR)),],
)
async def create_product(product_data: ProductCreate, conn=Depends(get_conn)):
    product_service = ProductService(conn)

    try:
        product = await product_service.create_product(product_data)

    except ValidationError as exc:
        detail = exc.errors()[0]
        raise HTTPException(status_code=422, detail=detail.get("msg"))

    return product


@router.delete(
    "/{product_id}",
    dependencies=[Depends(UserAndRoleChecker(UserRole.MODERATOR)),],
)
async def delete_product(product_id: PositiveInt, conn=Depends(get_conn)):
    product_service = ProductService(conn)
    deleted_product = await product_service.delete_product(product_id)
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"detail": f"Product deleted: {deleted_product}"}
