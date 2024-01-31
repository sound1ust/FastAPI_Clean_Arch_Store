import uuid

from fastapi import APIRouter, HTTPException, Cookie
from pydantic import PositiveInt

from app.models.users import UserOut, UserRole
from app.servises.users import UserService

router = APIRouter(
    prefix="/users",
    tags=["users", ],
)


@router.get("/user", response_model=UserOut)
def get_user_by_session_token(session_token: uuid.UUID = Cookie()):
    user_service = UserService()
    user = user_service.get_user_by_session_token(session_token)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
        )

    if user.role.value < UserRole.USER.value:
        raise HTTPException(
            status_code=403,
            detail="Forbidden",
        )

    return user


@router.get("/{user_id}", response_model=UserOut)
def get_user_by_id(user_id: PositiveInt, session_token: uuid.UUID = Cookie()):
    user_service = UserService()
    user = user_service.get_user_by_session_token(session_token)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
        )

    if user.role.value < UserRole.ADMIN.value:
        raise HTTPException(
            status_code=403,
            detail="Forbidden",
        )

    desired_user = user_service.get_user_by_id(user_id)

    return desired_user
