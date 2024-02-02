from pydantic import PositiveInt

from app.models.products import Product, ProductCreate
from app.repositories.products import ProductRepository


class ProductService(ProductRepository):
    async def create_product(self, product_data: ProductCreate):
        query = '''
        INSERT INTO products(name, category, price)
        VALUES ($1, $2, $3)
        RETURNING *;
        '''
        stored_data = await self.conn.fetchrow(
            query,
            product_data.name,
            product_data.category,
            product_data.price,
        )
        if not stored_data:
            return None

        product = Product(**{key: value for key, value in stored_data.items()})
        return product

    async def get_product_by_id(self, product_id: PositiveInt):
        query = '''
        SELECT *
        FROM products
        WHERE product_id = $1;
        '''
        stored_data = await self.conn.fetchrow(query, product_id)
        if not stored_data:
            return None

        product = Product(**{key: value for key, value in stored_data.items()})
        return product

    async def get_products_list(self, data: dict):
        keyword = data.get("keyword")
        category = data.get("category")
        limit = data.get("limit")

        params = ["%" + keyword + "%"]
        query = '''
        SELECT * FROM products 
        WHERE name ILIKE $1
        '''

        if category:
            query += '''
            AND category = $2
            '''
            params.append(category)

        query += '''
        ORDER BY product_id
        '''

        if limit:
            query += f'''
            LIMIT ${str(len(params) + 1)}
            '''
            params.append(limit)

        query += ";"

        products = await self.conn.fetch(query,*params)
        return products

    async def delete_product(self, product_id: PositiveInt):
        query = '''
            DELETE FROM products WHERE product_id = $1 RETURNING *;
            '''
        deleted_product = await self.conn.fetchrow(query, product_id)
        if not deleted_product:
            return None

        return deleted_product

    async def filter_products_by_category(self, category):
        query = '''
            SELECT * FROM products WHERE category = $1;
            '''
        products = await self.conn.fetch(query, category)
        if not products:
            return None

        return products
