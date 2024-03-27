import os

from app.repositories.products import ProductPostgresqlRepository

# database settings based on environment variables
DATABASE_SETTINGS = {
    "REPOSITORY": "POSTGRES",
    "HOST": os.environ.get("HOST"),
    "PORT": os.environ.get("PORT"),
    "DB": os.environ.get("DB"),
    "DB_USERNAME": os.environ.get("DB_USERNAME"),
    "DB_PASSWORD": os.environ.get("DB_PASSWORD"),
}

# Repositories by database system and sub app name
REPOSITORIES = {
    "POSTGRES": {
        "PRODUCT": ProductPostgresqlRepository,
    },
}