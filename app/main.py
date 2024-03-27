import asyncpg
import uvicorn
from fastapi import FastAPI

from app.routers.v1 import auth, users, products
from app.config import *

app = FastAPI()

app.include_router(users.router)
app.include_router(products.router)
app.include_router(auth.router)


@app.on_event("startup")
async def startup():
    app.state.pool = await asyncpg.create_pool(
        host=DATABASE_SETTINGS.get("HOST"),
        port=DATABASE_SETTINGS.get("PORT"),
        database=DATABASE_SETTINGS.get("DB"),
        user=DATABASE_SETTINGS.get("DB_USERNAME"),
        password=DATABASE_SETTINGS.get("DB_PASSWORD"),
    )


@app.on_event("shutdown")
async def shutdown():
    await app.state.pool.close()


@app.get("/test")
def test():
    return {"test": "OK"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host='0.0.0.0',
        port=8000,
        reload=True,
        workers=3
    )
