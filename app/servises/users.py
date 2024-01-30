from app.databases.users import USERS_DB
from app.repositories.users import UserRepository


class UserService(UserRepository):
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
