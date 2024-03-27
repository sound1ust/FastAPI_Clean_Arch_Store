import dotenv

from app.config import *

# tests requires .env file
env = dotenv.find_dotenv("../.env")

BASE_URL = "http://127.0.0.1:8000/api/" + ROUTERS_VERSION

# test database settings based on .env file
DATABASE_SETTINGS = {
    "REPOSITORY": "POSTGRES",
    "HOST":  dotenv.get_key(env, "HOST"),
    "PORT": dotenv.get_key(env, "PORT"),
    "DATABASE": dotenv.get_key(env, "DB"),
    "USER": dotenv.get_key(env, "DB_USERNAME"),
    "PASSWORD": dotenv.get_key(env, "DB_PASSWORD"),
}
