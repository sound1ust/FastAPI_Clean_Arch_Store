from fastapi import APIRouter, HTTPException, Request
from app.utils.headers import check_headers, validate_headers

router = APIRouter(
    prefix="/headers",
    tags=["headers",]
)


@router.get("")
async def get_headers(request: Request):
    expecting_headers = check_headers(request.headers)
    if expecting_headers:
        raise HTTPException(
            status_code=400,
            detail=f"Following headers are not found: {expecting_headers}",
        )

    if not validate_headers(request.headers):
        raise HTTPException(
            status_code=400,
            detail="Invalid request",
        )

    return {
        "User-Agent": request.headers["User-Agent"],
        "Accept-Language": request.headers["Accept-Language"],
    }
