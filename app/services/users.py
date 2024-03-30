from uuid import UUID

from pydantic import PositiveInt

from app.databases.users import USERS_DB
from app.repositories.users import UserRepository
from app.models.users import UserIn


class UserService(UserRepository):
    def save_user(self, user: UserIn):
        for user_data in USERS_DB:
            if user_data.get("user_id") == user.user_id:
                user_data.update(user.model_dump())
                return user

        return None

    def get_user_by_id(self, user_id: PositiveInt):
        for user_data in USERS_DB:
            if user_data.get("user_id") == user_id:
                return UserIn(**user_data)

        return None

    def get_user_by_username(self, username: str):
        for user_data in USERS_DB:
            if user_data.get("username") == username:
                return UserIn(**user_data)

        return None

    def get_user_by_username_and_password(self, username: str, password: str):
        for user_data in USERS_DB:
            if (user_data.get("username") == username and
                    user_data.get("password") == password):
                return UserIn(**user_data)

        return None

    def get_user_by_session_token(self, session_token: UUID):
        for user_data in USERS_DB:
            if user_data.get("session_token") == session_token:
                return UserIn(**user_data)

        return None

    def delete_user(self, user_id: PositiveInt):
        for user_data in USERS_DB:
            if user_data.get("user_id") == user_id:
                USERS_DB.remove(user_data)
                return True

        return False
