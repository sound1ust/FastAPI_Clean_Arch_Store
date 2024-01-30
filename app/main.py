import uvicorn
from fastapi import FastAPI
from app.routers import users
from app.routers import products
from app.routers import headers
from app.routers import auth

app = FastAPI()

app.include_router(users.router)
app.include_router(products.router)
app.include_router(headers.router)
app.include_router(auth.router)


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host='127.0.0.1',
        port=8000,
        reload=True,
        workers=3
    )
