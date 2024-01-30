from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from starlette import status
import jwt

from app.servises.users import UserService
from app.databases.tokens import TOKEN_BLACKLIST

security = HTTPBasic()

SECRET_KEY = "secret"
ALGORITHM = "HS256"


def authenticate_user(credentials: HTTPBasicCredentials = Depends(security)):
    user_service = UserService()
    user = user_service.get_user_by_username(credentials.username)
    if not user or user.password != credentials.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    return user


def create_jwt_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)


def authenticate_user_jwt(token: str):
    if token in TOKEN_BLACKLIST:
        return False

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        TOKEN_BLACKLIST.append(token)
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return False

    user_service = UserService()
    user = user_service.get_user_by_username_and_password(
        payload.get("username"),
        payload.get("password"),
    )

    if not user:
        return False

    return True
