import asyncpg
import uvicorn
from fastapi import FastAPI
import dotenv

from app.routers import users
from app.routers import products
from app.routers import auth
from app.settings import DATABASE_URL

app = FastAPI()

app.include_router(users.router)
app.include_router(products.router)
app.include_router(auth.router)


@app.on_event("startup")
async def startup():
    app.state.pool = await asyncpg.create_pool(DATABASE_URL)


@app.on_event("shutdown")
async def shutdown():
    await app.state.pool.close()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host='127.0.0.1',
        port=8000,
        reload=True,
        workers=3
    )
