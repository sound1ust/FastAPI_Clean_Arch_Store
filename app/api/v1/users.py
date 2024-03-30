import uuid

from fastapi import APIRouter, HTTPException, Cookie, Depends, Request
from pydantic import PositiveInt

from app.dependencies.auth import UserAndRoleChecker
from app.models.users import UserOut, UserRole, UserIn
from app.services.users import UserService

router = APIRouter(
    prefix="/api/v1/users",
    tags=["users", ],
)


@router.get(
    "/user",
    response_model=UserOut,
)
def get_user_by_session_token(
        user: UserIn = Depends(UserAndRoleChecker(UserRole.USER))
):
    return user


@router.get(
    "/{user_id}",
    response_model=UserOut,
    dependencies=[Depends(UserAndRoleChecker(UserRole.ADMIN)),]
)
def get_user_by_id(user_id: PositiveInt):
    user_service = UserService()
    desired_user = user_service.get_user_by_id(user_id)

    return desired_user


@router.delete(
    "/{user_id}",
    dependencies=[Depends(UserAndRoleChecker(UserRole.ADMIN)),],
)
def delete_user(
        user_id: PositiveInt,
):
    user_service = UserService()
    if not user_service.delete_user(user_id):
        raise HTTPException(status_code=404, detail="User not found")

    return {"detail": "User deleted"}
