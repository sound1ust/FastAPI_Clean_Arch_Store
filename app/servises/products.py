from pydantic import PositiveInt

from app.databases.products import PRODUCTS_DB
from app.models.products import ProductSearch, Product
from app.repositories.products import ProductRepository


class ProductService(ProductRepository):
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

    @staticmethod
    def filter_products_by_category(category):
        return [
            product for product in PRODUCTS_DB
            if product.get("category") == category
        ]
