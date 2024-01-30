from uuid import UUID
from typing import Union
from pydantic import BaseModel, PositiveInt


class UserIn(BaseModel):
    user_id: PositiveInt
    username: str
    password: str
    role: int
    session_token: Union[UUID, None] = None


class UserOut(BaseModel):
    user_id: PositiveInt
    username: str


class UserLogin(BaseModel):
    username: str
    password: str
