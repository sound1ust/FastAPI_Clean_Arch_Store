from fastapi import HTTPException

from app.routers.products import get_product, list_products


def test_get_product_valid_id():
    product_id = 123
    product = get_product(product_id)
    assert product_id == product.get("product_id")


def test_get_product_invalid_id():
    product_id = 1

    try:
        get_product(product_id)

    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == f"There are no products with id '{product_id}'"


def test_list_products_no_category_no_limit():
    keyword = "phone"
    products = list_products(keyword)
    assert all(
        keyword in str(product.get("name").lower()) for product in products
    )


def test_list_products_with_category_no_limit():
    keyword = "phone"
    category = "Electronics"
    products = list_products(keyword, category)
    assert all(
        keyword in str(product.get("name").lower()) for product in products
    )


def test_list_products_no_category_with_limit():
    keyword = "phone"
    limit = 2
    products = list_products(keyword, limit=limit)
    assert len(products) == limit
    assert all(
        keyword in str(product.get("name").lower()) for product in products
    )


def test_list_products_invalid_category():
    keyword = "phone"
    category = "invalid_category"

    try:
        list_products(keyword, category)

    except HTTPException as exc:
        assert exc.status_code == 422
        assert exc.detail == (
            f"Value error, There is no category '{category}' in the products"
        )


def test_list_products_no_matching_products():
    keyword = "invalid_keyword"

    try:
        list_products(keyword)
        pass

    except HTTPException as exc:
        assert exc.status_code == 404
        assert exc.detail == (
            f"There are no products with these parameters"
        )
