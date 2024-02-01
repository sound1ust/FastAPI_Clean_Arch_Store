from enum import Enum
from uuid import UUID
from typing import Union
from pydantic import BaseModel, PositiveInt


class UserRole(Enum):
    USER = 1
    MODERATOR = 2
    ADMIN = 3


class UserIn(BaseModel):
    user_id: PositiveInt
    username: str
    password: str
    role: UserRole
    session_token: Union[UUID, None] = None


class UserOut(BaseModel):
    user_id: PositiveInt
    username: str


class UserLogin(BaseModel):
    username: str
    password: str
