from fastapi import APIRouter, Query, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from src.services.user import UserDAO
from src.core.exceptions import LoginException, UserAlreadyExistsException
from src.schemas.token import SToken
from src.core.config import settings
from src.services.auth import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register")
async def register(
        username: Annotated[str, Query(description="Логин")],
        password: Annotated[str, Query(description="Пароль")]
):
    exist_user = await UserDAO.find_one_or_none(username=username)
    if exist_user is not None:
        raise UserAlreadyExistsException
    hash_password = await AuthService.get_password_hash(password=password)
    await UserDAO.add(username=username, hash_password=hash_password)
    return {"msg": "Account has been created"}


@router.post("/token", response_model=SToken)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await AuthService.authenticate_user(
        username=form_data.username,
        password=form_data.password
    )
    if not user:
        raise LoginException
    access_token_expire = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )
    access_token = await AuthService.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expire
    )
    return SToken(access_token=access_token, token_type="bearer")


@router.get("/protected")
async def protected_route(user: dict = Depends(AuthService.get_current_user)):
    return {"message": "Вы вошли!", "username": user.username}
