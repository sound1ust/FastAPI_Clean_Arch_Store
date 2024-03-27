from abc import ABC, abstractmethod
from uuid import UUID

import asyncpg
from pydantic import PositiveInt

from app.models.users import UserIn


class UserRepository(): # UserAbstractRepository
    @abstractmethod
    def save_user(self, user: UserIn):
        ...

    @abstractmethod
    def get_user_by_id(self, user_id: PositiveInt):
        ...

    @abstractmethod
    def get_user_by_username(self, username: str):
        ...

    @abstractmethod
    def get_user_by_username_and_password(self, username: str, password: str):
        ...

    @abstractmethod
    def get_user_by_session_token(self, session_token: UUID):
        ...

    @abstractmethod
    def delete_user(self, user_id: PositiveInt):
        ...
