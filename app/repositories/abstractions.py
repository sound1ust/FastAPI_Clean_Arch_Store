from abc import ABC

import asyncpg


class AbstractRepository(ABC):
    def __init__(self, conn: asyncpg.Connection):  # TODO AbstractConnection
        self.conn = conn
