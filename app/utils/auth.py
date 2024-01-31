import uuid

from fastapi.security import HTTPBasic
import jwt

from app.models.users import UserRole
from app.servises.users import UserService
from app.databases.tokens import TOKEN_BLACKLIST

security = HTTPBasic()

SECRET_KEY = "secret"
ALGORITHM = "HS256"


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

    return user


def set_session_token_cookie(response):
    session_token = uuid.uuid4()
    response.set_cookie(
        key="session_token",
        value=session_token,
        httponly=True,
        max_age=120,
    )
    return session_token
