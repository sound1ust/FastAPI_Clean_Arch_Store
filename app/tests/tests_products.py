import json
from fastapi import HTTPException
from httpx import AsyncClient

from app.config import BASE_URL
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
