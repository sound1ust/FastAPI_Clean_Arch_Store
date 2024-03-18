
import asyncpg
import pytest
from fastapi import HTTPException
from httpx import AsyncClient

from app.routers import get_product, list_products
from app.main import app
from app.settings import DATABASE_URL


# TODO
@pytest.fixture
async def set_up():
    ...


# TODO: clean db after every test?
@pytest.mark.asyncio
async def test_get_product_valid_id():
    app.state.pool = await asyncpg.create_pool(DATABASE_URL)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(
            f"/products",
            json={
                "name": "test",
                "category": "test",
                "price": 1,
            })

        product_id = 1
        response = await ac.get(f"/products/{product_id}")
        assert response.status_code == 200

    await app.state.pool.close()


@pytest.mark.asyncio
async def test_get_product_invalid_id():
    app.state.pool = await asyncpg.create_pool(DATABASE_URL)
    async with AsyncClient(app=app, base_url="http://test") as ac:
        await ac.post(
            f"/products",
            json={
                "name": "test",
                "category": "test",
                "price": 1,
            })

        product_id = 100

        try:
            await ac.get(f"/products/{product_id}")

        except HTTPException as exc:
            assert exc.status_code == 404
            assert exc.detail == f"There are no products with id '{product_id}'"

    await app.state.pool.close()


async def test_list_products_no_category_no_limit():
    keyword = "phone"
    products = await list_products(keyword)
    assert all(
        keyword in str(product.get("name").lower()) for product in products
    )


async def test_list_products_with_category_no_limit():
    keyword = "phone"
    category = "Electronics"
    products = await list_products(keyword, category)
    assert all(
        keyword in str(product.get("name").lower()) for product in products
    )


async def test_list_products_no_category_with_limit():
    keyword = "phone"
    limit = 2
    products = await list_products(keyword, limit=limit)
    assert len(products) == limit
    assert all(
        keyword in str(product.get("name").lower()) for product in products
    )


async def test_list_products_invalid_category():
    keyword = "phone"
    category = "invalid_category"

    try:
        await list_products(keyword, category)

    except HTTPException as exc:
        assert exc.status_code == 422
        assert exc.detail == (
            f"Value error, There is no category '{category}' in the products"
        )


async def test_list_products_no_matching_products():
    keyword = "invalid_keyword"

    try:
        await list_products(keyword)
        pass

    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == (
            f"There are no products with these parameters"
        )
