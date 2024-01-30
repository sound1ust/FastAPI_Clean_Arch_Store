from app.models.users import UserIn

USERS_DB = [
    UserIn(**{
        "user_id": 1,
        "username": "admin",
        "password": "1234",
    }),
    UserIn(**{
        "user_id": 2,
        "username": "string",
        "password": "string",
    }),
    UserIn(**{
        "user_id": 3,
        "username": "qwert",
        "password": "1111",
    }),
    UserIn(**{
        "user_id": 4,
        "username": "pavel",
        "password": "0000",
    }),
]
