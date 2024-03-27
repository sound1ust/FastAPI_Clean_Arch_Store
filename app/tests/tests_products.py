import json
from fastapi import HTTPException
from httpx import AsyncClient

from app.tests.config import BASE_URL
from app.tests.fixtures import *


# GET
@pytest.mark.asyncio
async def test_get_product_valid_id(
        pool,
        product: Product,
):
    pool = await pool
    product = await product
    async with pool:
        async with AsyncClient(app=app) as ac:
            response = await ac.get(f"{BASE_URL}/products/{product.product_id}")
            assert response.status_code == 200
            assert product.dict() == json.loads(response.content)


@pytest.mark.asyncio
async def test_get_product_invalid_id(
        pool,
):
    pool = await pool
    id = 0
    async with pool:
        async with AsyncClient(app=app) as ac:
            try:
                response = await ac.get(f"{BASE_URL}/products/{id}")
            except HTTPException as exc:
                assert exc.status_code == 404
                assert exc.detail == f"There are no products with id '{id}'"


# LIST
@pytest.mark.asyncio
async def test_list_products_no_keyword_no_category_no_limit(
        pool,
        product: Product,
        product_2: Product,
):
    pool = await pool
    product = await product
    product_2 = await product_2
    async with pool:
        async with AsyncClient(app=app) as ac:
            response = await ac.get(f"{BASE_URL}/products")
            assert response.status_code == 200
            assert len(json.loads(response.content)) == 2
            assert product.dict() == json.loads(response.content)[0]


@pytest.mark.asyncio
async def test_list_products_with_keyword_no_category_no_limit(
        pool,
        product: Product,
        product_2: Product,
):
    pool = await pool
    product = await product
    product_2 = await product_2
    async with pool:
        async with AsyncClient(app=app) as ac:
            response = await ac.get(f"{BASE_URL}/products?keyword={product.name}")
            assert response.status_code == 200
            assert len(json.loads(response.content)) == 1
            assert product.dict() == json.loads(response.content)[0]


@pytest.mark.asyncio
async def test_list_products_with_keyword_with_category_no_limit(
        pool,
        product: Product,
        product_2: Product,
):
    pool = await pool
    product = await product
    product_2 = await product_2
    async with pool:
        async with AsyncClient(app=app) as ac:
            response = await ac.get(f"{BASE_URL}/products?keyword={product.name}&category={product.category}")
            assert response.status_code == 200
            assert len(json.loads(response.content)) == 1
            assert product.dict() == json.loads(response.content)[0]


@pytest.mark.asyncio
async def test_list_products_no_keyword_no_category_with_limit(
        pool,
        product: Product,
        product_2: Product,
):
    pool = await pool
    product = await product
    product_2 = await product_2
    async with pool:
        async with AsyncClient(app=app) as ac:
            response = await ac.get(f"{BASE_URL}/products?limit=1")
            assert response.status_code == 200
            assert len(json.loads(response.content)) == 1
            assert product.dict() == json.loads(response.content)[0]


@pytest.mark.asyncio
async def test_list_products_invalid_category(
        pool,
):
    pool = await pool
    category = "invalid"
    async with pool:
        async with AsyncClient(app=app) as ac:
            try:
                response = await ac.get(f"{BASE_URL}/products?category={category}")

            except HTTPException as exc:
                assert exc.status_code == 422
                assert exc.detail == (
                    f"Value error, There is no category '{category}' in the products"
                )


@pytest.mark.asyncio
async def test_list_products_not_found(
        pool,
):
    pool = await pool
    async with pool:
        async with AsyncClient(app=app) as ac:
            try:
                response = await ac.get(f"{BASE_URL}/products")

            except HTTPException as exc:
                assert exc.status_code == 404
                assert exc.detail == (
                    f"There are no products with these parameters"
                )


# CREATE
@pytest.mark.asyncio
async def test_create_product_valid_data(
        pool,
):
    pool = await pool
    data = {
        "name": "test",
        "category": "test",
        "price": 1000
    }

    async with pool:
        async with AsyncClient(app=app) as ac:
            response = await ac.post(
                f"{BASE_URL}/products",
                json={
                    "name": data.get("name"),
                    "category": data.get("category"),
                    "price": data.get("price")
                }
            )
            assert response.status_code == 201
            product_obj = json.loads(response.content)
            assert product_obj["name"] == data.get("name")
            assert product_obj["category"] == data.get("category")
            assert product_obj["price"] == data.get("price")


@pytest.mark.asyncio
async def test_create_product_invalid_data(
        pool,
):
    pool = await pool
    data = {
        "name": "",  # name is empty
        "category": "test",
        "price": 1000
    }

    async with pool:
        async with AsyncClient(app=app) as ac:
            try:
                response = await ac.post(
                    f"{BASE_URL}/products",
                    json={
                        "name": data.get("name"),
                        "category": data.get("category"),
                        "price": data.get("price")
                    }
                )
            except HTTPException as exc:
                assert exc.status_code == 422
                assert exc.detail == "Validation error: name is too short"


# DELETE
@pytest.mark.asyncio
async def test_delete_product_valid_id(
        pool,
        product: Product,
):
    pool = await pool
    product = await product

    async with pool:
        async with AsyncClient(app=app) as ac:
            response = await ac.delete(f"{BASE_URL}/products/{product.product_id}")
            assert response.status_code == 200
            assert json.loads(response.content) == {
                'detail': f"Product deleted: "
                          f"product_id={product.product_id} "
                          f"name='{product.name}' "
                          f"category='{product.category}' "
                          f"price={product.price}"
            }

            try:
                response = await ac.get(f"{BASE_URL}/products/{product.product_id}")
            except HTTPException as exc:
                assert exc.status_code == 404
                assert exc.detail == f"There are no products with id '{product.product_id}'"


@pytest.mark.asyncio
async def test_delete_product_invalid_id(
        pool,
):
    pool = await pool
    id = 0  # invalid id
    async with pool:
        async with AsyncClient(app=app) as ac:
            try:
                response = await ac.delete(f"{BASE_URL}/products/{id}")
            except HTTPException as exc:
                assert exc.status_code == 404
                assert exc.detail == f"There are no products with id '{id}'"
