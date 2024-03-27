from typing import List

from asyncpg import UniqueViolationError, Record

from app.repositories.abstract import AbstractRepository
from app.models.exceptions import (
    ProductNotFoundException,
    ProductsListNotFoundException,
    ProductNotCreatedException,
    ProductExistsException,
)
from app.repositories.exceptions import RepositoryConfigException


class ProductPostgresqlRepository(AbstractRepository):
    """
    Postgresql-compatible repository that initialises with asyncpg.Connection.
    """
    def __init__(self, config):
        super().__init__(config)
        self.conn = config.get("conn")
        if not self.conn:
            raise RepositoryConfigException

    async def create(self, name, category, price) -> Record:
        """
        Takes arguments and makes an INSERT request to a Database.
        """
        query = '''
        INSERT INTO products(name, category, price)
        VALUES ($1, $2, $3)
        RETURNING *;
        '''
        try:
            stored_data = await self.conn.fetchrow(
                query, name, category, price,
            )
        except UniqueViolationError as exc:
            raise ProductExistsException(name=name)

        if not stored_data:
            raise ProductNotCreatedException()

        return stored_data

    async def get(self, product_id) -> Record:
        """
        Takes product_id and makes a SELECT request to a Database.
        """
        query = '''
        SELECT product_id, name, category, price
        FROM products
        WHERE product_id = $1;
        '''
        stored_data = await self.conn.fetchrow(query, product_id)
        if not stored_data:
            raise ProductNotFoundException(product_id=product_id)

        return stored_data

    async def list(self, keyword, category, limit) -> List[Record]:
        """
        Takes arguments and makes a SELECT request to a Database.
        """
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

        stored_data = await self.conn.fetch(query, *params)
        if not stored_data:
            raise ProductsListNotFoundException()

        return stored_data

    async def update(self, product_id, name, category, price) -> Record:
        """
        Takes product_id and makes an UPDATE request to a Database.
        """
        query = '''
        UPDATE products
        SET name = $1, category = $2, price = $3
        WHERE product_id = $4
        RETURNING *;
        '''
        try:
            stored_data = await self.conn.fetchrow(
                query, name, category, price, product_id,
            )
        except UniqueViolationError as exc:
            raise ProductExistsException(name=name)

        if not stored_data:
            raise ProductNotFoundException(product_id=product_id)

        return stored_data

    async def delete(self, product_id) -> Record:
        """
        Takes product_id and makes a DELETE request to a Database.
        """
        query = '''
        DELETE FROM products WHERE product_id = $1 RETURNING *;
        '''
        stored_data = await self.conn.fetchrow(query, product_id)
        if not stored_data:
            raise ProductNotFoundException(product_id=product_id)

        return stored_data
