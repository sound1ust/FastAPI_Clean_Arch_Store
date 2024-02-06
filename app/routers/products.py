from fastapi import APIRouter, HTTPException, Depends
from pydantic import PositiveInt, ValidationError

from app.dependencies.auth import UserAndRoleChecker
from app.models.products import ProductSearch, Product, ProductCreate
from app.models.users import UserRole
from app.servises.products import ProductService
from database.dependencies import get_conn

router = APIRouter(
    prefix="/products",
    tags=["products", ],
)

@router.post(
    "",
    response_model=Product,
    # dependencies=[Depends(UserAndRoleChecker(UserRole.MODERATOR)), ],
)
async def create_product(product_data: ProductCreate, conn=Depends(get_conn)):
    name = product_data.name
    category = product_data.category
    price = product_data.price

    product_service = ProductService(conn)
    product = await product_service.create(name, category, price)
    if not product:
        raise HTTPException(status_code=400, detail="Bad Request")

    return product

@router.get("")
async def list_products(
        product_search: ProductSearch = Depends(),
        conn=Depends(get_conn),
):
    keyword = product_search.keyword
    category = product_search.category
    limit = product_search.limit

    product_service = ProductService(conn)
    products = await product_service.list(keyword, category, limit)

    if not products:
        raise HTTPException(
            status_code=404,
            detail="There are no products with these parameters",
        )

    return products


@router.get("/{product_id}", response_model=Product)
async def get_product(product_id: PositiveInt, conn=Depends(get_conn)):
    product_service = ProductService(conn)
    product = await product_service.get(product_id)

    if not product:
        raise HTTPException(
            status_code=404,
            detail=f"There are no products with id '{product_id}'",
        )

    return product

@router.post(
    "/{product_id}",
    response_model=Product,
    # dependencies=[Depends(UserAndRoleChecker(UserRole.MODERATOR)), ],
)
async def update_product(
        product_id: PositiveInt,
        product_data: ProductCreate,
        conn=Depends(get_conn),
):
    name = product_data.name
    category = product_data.category
    price = product_data.price

    product_service = ProductService(conn)
    product = await product_service.update(product_id, name, category, price)

    if not product:
        raise HTTPException(
            status_code=404,
            detail=f"There are no products with id '{product_id}'",
        )

    return product


@router.delete(
    "/{product_id}",
    # dependencies=[Depends(UserAndRoleChecker(UserRole.MODERATOR)), ],
)
async def delete_product(product_id: PositiveInt, conn=Depends(get_conn)):
    product_service = ProductService(conn)
    deleted_product = await product_service.delete(product_id)
    if not deleted_product:
        raise HTTPException(status_code=404, detail="Product not found")

    return {"detail": f"Product deleted: {deleted_product}"}
