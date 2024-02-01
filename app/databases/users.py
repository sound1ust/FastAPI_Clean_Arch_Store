from app.models.users import UserRole

USERS_DB = [
    {
        "user_id": 1,
        "username": "admin",
        "password": "1234",
        "role": UserRole.ADMIN,
    },
    {
        "user_id": 2,
        "username": "moder",
        "password": "1234",
        "role": UserRole.USER,
    },
    {
        "user_id": 3,
        "username": "user",
        "password": "1234",
        "role": UserRole.USER,
    },
]