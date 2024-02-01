import uuid

from fastapi import HTTPException, Request

from app.models.users import UserRole
from app.servises.users import UserService


class UserAndRoleChecker:
    def __init__(self, acceptable_role: UserRole = None):
        self.acceptable_role = acceptable_role

    def __call__(self, request: Request):
        try:
            session_token = uuid.UUID(request.cookies.get("session_token"))
        except (ValueError, TypeError) as exc:
            raise HTTPException(
                status_code=401,
                detail="Unauthorized",
            )

        user_service = UserService()
        user = user_service.get_user_by_session_token(session_token)

        if not user:
            raise HTTPException(
                status_code=401,
                detail="Unauthorized",
            )

        if not self.acceptable_role:
            return user

        if user.role.value < self.acceptable_role.value:
            raise HTTPException(
                status_code=403,
                detail="Forbidden",
            )

        return user
