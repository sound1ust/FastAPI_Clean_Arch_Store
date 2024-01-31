import time
import uuid

from fastapi import APIRouter, HTTPException, Cookie, Response

from app.models.users import UserLogin
from app.utils.auth import (
    create_jwt_token,
    authenticate_user_jwt,
    set_session_token_cookie,
)
from app.servises.users import UserService

router = APIRouter(
    prefix="/auth",
    tags=["auth", ],
)


@router.post("/login")
def jwt_login(data: UserLogin):
    user_service = UserService()
    user = user_service.get_user_by_username_and_password(
        data.username,
        data.password,
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    token = create_jwt_token(
        {
            "username": data.username,
            "password": data.password,
            "exp": time.time() + 3600,
        },
    )
    return {"access_token": token}


@router.get("/logout")
def jwt_logout(session_token: uuid.UUID = Cookie()):
    user_service = UserService()
    user = user_service.get_user_by_session_token(session_token)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
        )

    user.session_token = None

    return {"detail": "You are logged out."}


@router.get("/authorize")
def jwt_authorize(token: str, response: Response):
    user_service = UserService()
    user = authenticate_user_jwt(token)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Token is invalid or expired."
        )

    session_token = set_session_token_cookie(response)
    user.session_token = session_token
    user_service.save_user(user)

    return {"detail": "You are authorized."}
