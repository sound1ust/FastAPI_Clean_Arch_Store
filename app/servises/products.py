from pydantic import PositiveInt

from app.databases.products import PRODUCTS_DB
from app.models.products import Product, ProductCreate
from app.repositories.products import ProductRepository


class ProductService(ProductRepository):
    def create_product(self, data: ProductCreate):
        product = Product(
            **data.model_dump(),
            product_id=self.get_highest_id() + 1,
        )
        PRODUCTS_DB.append(product.model_dump())
        return product

    def get_product_by_id(self, product_id: PositiveInt):
        for product_data in PRODUCTS_DB:
            if product_data.get("product_id") == product_id:
                return Product(**product_data)

        return None

    def get_products_list(self, data: dict):
        result = []
        index = 0

        products = PRODUCTS_DB

        if data.get("category"):
            products = self.filter_products_by_category(data.get("category"))

        while len(result) < data.get("limit") and index < len(products):
            product_data = products[index]

            if data.get("keyword").lower() in product_data.get("name").lower():
                result.append(Product(**product_data))

            index += 1

        return result

    def delete_product(self, product_id: PositiveInt):
        for product_data in PRODUCTS_DB:
            if product_data.get("product_id") == product_id:
                PRODUCTS_DB.remove(product_data)
                return True

        return False

    @staticmethod
    def filter_products_by_category(category):
        return [
            product for product in PRODUCTS_DB
            if product.get("category") == category
        ]

    @staticmethod
    def get_highest_id():
        return max(product.get("product_id") for product in PRODUCTS_DB)
