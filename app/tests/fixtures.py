import contextlib

import asyncpg
import pytest

from app.main import app
from app.tests.config import *
from app.models.exceptions import ProductExistsException
from app.models.products import Product
from app.services.product import ProductService


@pytest.fixture
async def pool():
    app.state.pool = await asyncpg.create_pool(
        host=DATABASE_SETTINGS.get("HOST"),
        port=DATABASE_SETTINGS.get("PORT"),
        database=DATABASE_SETTINGS.get("DATABASE"),
        user=DATABASE_SETTINGS.get("USER"),
        password=DATABASE_SETTINGS.get("PASSWORD"),
    )
    async with app.state.pool.acquire() as connection:
        await connection.execute(f"DELETE FROM products")

    @contextlib.asynccontextmanager
    async def cleanup():
        try:
            yield app.state.pool
        finally:
            async with app.state.pool.acquire() as connection:
                await connection.execute(f"DELETE FROM products")
            await app.state.pool.close()

    return cleanup()


@pytest.fixture
async def product(pool) -> Product:
    async with app.state.pool.acquire() as connection:
        return await create_product(name="test", connection=connection)


@pytest.fixture
async def product_2(pool) -> Product:
    async with app.state.pool.acquire() as connection:
        return await create_product(name="phone", connection=connection)


async def create_product(connection, name):
    product_service = ProductService(conn=connection)
    while True:
        try:
            product = await product_service.create(
                name=name,
                category=name,
                price=1000
            )
            return product
        except ProductExistsException as exc:
            connection.execute(f"DELETE FROM products WHERE name = '{name}'")
