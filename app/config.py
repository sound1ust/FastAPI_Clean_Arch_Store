import dotenv

env = dotenv.find_dotenv("../.env")


BASE_URL = dotenv.get_key(env, "BASE_URL")

HOST = dotenv.get_key(env, "HOST")
PORT = dotenv.get_key(env, "PORT")
DATABASE = dotenv.get_key(env, "DB")
USER = dotenv.get_key(env, "DB_USERNAME")
PASSWORD = dotenv.get_key(env, "DB_PASSWORD")