from uuid import UUID

from app.databases.users import USERS_DB
from app.repositories.users import UserRepository


class UserService(UserRepository):
    ROLES = {
        "user": 1,
        "admin": 2,
    }

    def get_user_by_id(self, user_id: int):
        for user in USERS_DB:
            if user.user_id == user_id:
                return user

        return None

    def get_user_by_username(self, username: str):
        for user in USERS_DB:
            if user.username == username:
                return user

        return None

    def get_user_by_username_and_password(self, username: str, password: str):
        for user in USERS_DB:
            if user.username == username and user.password == password:
                return user

        return None

    def get_user_by_session_token(self, session_token: UUID):
        for user in USERS_DB:
            if user.session_token == session_token:
                return user

        return None

