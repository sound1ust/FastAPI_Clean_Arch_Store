import json
from httpx import AsyncClient

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
            response = await ac.get(
                f"{BASE_URL}/products/{product.product_id}"
            )
            assert response.status_code == 200
            assert product.dict() == json.loads(response.content)


@pytest.mark.asyncio
async def test_get_product_invalid_id(
        pool,
):
    pool = await pool
    id = 1
    async with pool:
        async with AsyncClient(app=app) as ac:
            response = await ac.get(f"{BASE_URL}/products/{id}")
            assert response.status_code == 404
            assert json.loads(response.content) == {
                "detail": f"There are no products with this id: {id}"
            }


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
            assert product_2.dict() == json.loads(response.content)[1]


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
            response = await ac.get(
                f"{BASE_URL}/products?keyword={product.name}"
            )
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
            response = await ac.get(
                f"{BASE_URL}/products?keyword={product.name}"
                f"&category={product.category}"
            )
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
async def test_list_products_not_found(
        pool,
):
    pool = await pool
    async with pool:
        async with AsyncClient(app=app) as ac:
            response = await ac.get(f"{BASE_URL}/products")
            assert response.status_code == 404
            assert json.loads(response.content) == {
                "detail": "There are no products with these parameters"
            }


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
            response = await ac.post(f"{BASE_URL}/products", json=data)
            assert response.status_code == 201
            id = json.loads(response.content).get("product_id")

            response_2 = await ac.get(f"{BASE_URL}/products/{id}")
            assert response_2.status_code == 200
            product_obj = json.loads(response_2.content)
            assert product_obj.get("name") == data.get("name")
            assert product_obj.get("category") == data.get("category")
            assert product_obj.get("price") == data.get("price")


@pytest.mark.asyncio
async def test_create_product_short_name(
        pool,
):
    pool = await pool
    data = {
        "name": "",
        "category": "test",
        "price": 1000
    }

    async with pool:
        async with AsyncClient(app=app) as ac:
            response = await ac.post(f"{BASE_URL}/products", json=data)
            assert response.status_code == 422
            assert json.loads(response.content).get("detail")[0].get(
                "msg") == "String should have at least 3 characters"


@pytest.mark.asyncio
async def test_create_product_short_category(
        pool,
):
    pool = await pool
    data = {
        "name": "test",
        "category": "",
        "price": 1000
    }

    async with pool:
        async with AsyncClient(app=app) as ac:
            response = await ac.post(f"{BASE_URL}/products", json=data)
            assert response.status_code == 422
            assert json.loads(response.content).get("detail")[0].get(
                "msg") == "String should have at least 3 characters"


@pytest.mark.asyncio
async def test_create_product_non_positive_price(
        pool,
):
    pool = await pool
    data = {
        "name": "test",
        "category": "test",
        "price": 0
    }

    async with pool:
        async with AsyncClient(app=app) as ac:
            response = await ac.post(f"{BASE_URL}/products", json=data)
            assert response.status_code == 422
            assert json.loads(response.content).get("detail")[0].get(
                "msg") == "Input should be greater than 0"


# UPDATE
@pytest.mark.asyncio
async def test_update_product_valid(
        pool,
        product: Product,
):
    pool = await pool
    product = await product
    data = {
        "name": "update",
        "category": "update",
        "price": 2000.0
    }

    async with pool:
        async with AsyncClient(app=app) as ac:
            response = await ac.post(
                f"{BASE_URL}/products/{product.product_id}",
                json=data
            )
            assert response.status_code == 200

            response_2 = await ac.get(
                f"{BASE_URL}/products/{product.product_id}"
            )
            assert response_2.status_code == 200
            product_obj = json.loads(response_2.content)
            assert product_obj.get("name") == data.get("name")
            assert product_obj.get("category") == data.get("category")
            assert product_obj.get("price") == data.get("price")


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
            response = await ac.delete(
                f"{BASE_URL}/products/{product.product_id}")
            assert response.status_code == 200
            assert json.loads(response.content) == {
                'detail': f"Product deleted: "
                          f"product_id={product.product_id} "
                          f"name='{product.name}' "
                          f"category='{product.category}' "
                          f"price={product.price}"
            }

            response = await ac.get(
                f"{BASE_URL}/products/{product.product_id}"
            )
            assert response.status_code == 404
            assert json.loads(response.content) == {
                "detail": f"There are no products with this id: "
                          f"{product.product_id}"
            }


@pytest.mark.asyncio
async def test_delete_product_invalid_id(
        pool,
):
    pool = await pool
    id = 1
    async with pool:
        async with AsyncClient(app=app) as ac:
            response = await ac.delete(f"{BASE_URL}/products/{id}")
            assert response.status_code == 404
            assert json.loads(response.content) == {
                "detail": f"There are no products with this id: {id}"
            }
