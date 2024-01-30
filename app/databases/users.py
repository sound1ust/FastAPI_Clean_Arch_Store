from app.models.users import UserIn

USERS_DB = [
    UserIn(**{
        "user_id": 1,
        "username": "admin",
        "password": "1234",
        "role": 2,
    }),
    UserIn(**{
        "user_id": 2,
        "username": "string",
        "password": "string",
        "role": 1,
    }),
    UserIn(**{
        "user_id": 3,
        "username": "qwert",
        "password": "1111",
        "role": 1,
    }),
    UserIn(**{
        "user_id": 4,
        "username": "pavel",
        "password": "0000",
        "role": 1,
    }),
]
