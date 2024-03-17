import os

import asyncpg
import uvicorn
from fastapi import FastAPI

from app.routers import auth, products, users

app = FastAPI()

app.include_router(users.router)
app.include_router(products.router)
app.include_router(auth.router)


@app.on_event("startup")
async def startup():
    app.state.pool = await asyncpg.create_pool(
        host=os.environ.get("HOST"),
        port=os.environ.get("PORT"),
        database=os.environ.get("DB"),
        user=os.environ.get("DB_USERNAME"),
        password=os.environ.get("DB_PASSWORD"),
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
