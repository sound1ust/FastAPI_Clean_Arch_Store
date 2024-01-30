import uuid

from fastapi import APIRouter, HTTPException, Cookie, Response, Depends
from starlette import status

from app.databases.users import USERS_DB
from app.models.users import UserOut, UserLogin, UserIn
from app.utils.users import (
    authenticate_user,
    create_jwt_token,
    authenticate_user_jwt,
)

from app.servises.users import UserService

router = APIRouter(
    prefix="/users",
    tags=["users", ],
)


@router.post("/cookie_login", response_model=UserOut)
async def cookie_login(user_login: UserLogin, response: Response):
    username = user_login.username
    password = user_login.password

    for user in USERS_DB:
        if user.username == username \
                and user.password == password:

            session_token = uuid.uuid4()
            response.set_cookie(
                key="session_token",
                value=session_token,
                httponly=True,
                max_age=120,
            )
            user.session_token = session_token

            return user

        else:
            continue

    raise HTTPException(
        status_code=401,
        detail="Invalid credentials",
    )


@router.get("", response_model=UserOut)
def get_user(session_token: uuid.UUID = Cookie()):
    user = [
        item for item in USERS_DB if item.session_token == session_token
    ]

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Unauthorized",
        )

    return user[0]


@router.get("/base_auth_login")
def base_auth_login(user: UserIn = Depends(authenticate_user)):
    response = Response(
        content=f"You have access to the protected resource: {user}",
    )
    response.status_code = status.HTTP_202_ACCEPTED
    response.headers["WWW-Authentication"] = "Basic"
    return response


@router.post("/jwt_login")
def jwt_login(data: UserLogin):
    user_service = UserService()
    user = user_service.get_user_by_username_and_password(
        data.username,
        data.password,
    )

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials",
        )

    token = create_jwt_token(
        {"username": data.username, "password": data.password}
    )

    return {"access_token": token}


@router.get("/jwt_only_resource")
def get_resource(token = Depends(authenticate_user_jwt)):
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Token is invalid or expired."
        )

    return {"detail": "Secret information"}
