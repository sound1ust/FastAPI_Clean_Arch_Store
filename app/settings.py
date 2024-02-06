import dotenv

env_path = "../.env"
DATABASE_URL = dotenv.get_key(env_path, "DATABASE_URL")