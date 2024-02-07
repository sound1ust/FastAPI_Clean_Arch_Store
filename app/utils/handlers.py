from fastapi import Request
from fastapi.responses import JSONResponse

from app.main import app
from app.models.exceptions import ProductBaseException


@app.exception_handler(Exception)
def global_exception_handler(request: Request, exc: Exception):
    # TODO add logger
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"},
    )


@app.exception_handler(ProductBaseException)
def product_exception_handler(request: Request, exc: ProductBaseException):
    # TODO add logger
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.detail,
    )
