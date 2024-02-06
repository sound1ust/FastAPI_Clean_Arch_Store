from fastapi import HTTPException


class ProductBaseException(HTTPException):
    default_status_code = 400
    default_detail = "Product error"

    def __init__(self, status_code: int = None, detail: str = None):
        if not status_code:
            status_code = self.default_status_code
        if not detail:
            detail = self.default_detail
        super().__init__(status_code=status_code, detail=detail)


class ProductNotFoundException(ProductBaseException):
    default_status_code = 404

    def __init__(self, product_id: int):
        detail = f"There are no products with this id: {product_id}"
        super().__init__(status_code=self.default_status_code, detail=detail)


class ProductsListNotFoundException(ProductBaseException):
    default_status_code = 404
    default_detail = "There are no products with these parameters"


class ProductNotCreatedException(ProductBaseException):
    default_status_code = 400
    default_detail = "Bad request"


class ProductExistsException(ProductBaseException):
    def __init__(self, name: str):
        detail = f"Product {name} is already exists"
        super().__init__(status_code=self.default_status_code, detail=detail)
