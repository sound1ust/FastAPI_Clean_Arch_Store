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
        "username": "string",
        "password": "string",
        "role": UserRole.USER,
    },
    {
        "user_id": 3,
        "username": "qwert",
        "password": "1111",
        "role": UserRole.USER,
    },
    {
        "user_id": 4,
        "username": "pavel",
        "password": "0000",
        "role": UserRole.USER,
    },
]