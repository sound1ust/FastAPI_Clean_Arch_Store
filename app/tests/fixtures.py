import contextlib

import asyncpg
import pytest

from app.main import app
from app.config import *
from app.models.exceptions import ProductExistsException
from app.models.products import Product
from app.servises.products import ProductService


@pytest.fixture
async def pool():
    app.state.pool = await asyncpg.create_pool(
        host=HOST,
        port=PORT,
        database=DATABASE,
        user=USER,
        password=PASSWORD,
    )

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
        product_service = ProductService(connection)

        while True:
            try:
                product = await product_service.create(
                    "test",
                    "test",
                    1000
                )
                return product
            except ProductExistsException as exc:
                connection.execute(f"DELETE FROM products WHERE name = 'test'")


@pytest.fixture
async def product_2(pool) -> Product:
    async with app.state.pool.acquire() as connection:
        product_service = ProductService(connection)

        while True:
            try:
                product = await product_service.create(
                    "phone",
                    "phone",
                    2000
                )
                return product
            except ProductExistsException as exc:
                connection.execute(f"DELETE FROM products WHERE name = 'phone'")
