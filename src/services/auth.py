from abc import ABC, abstractmethod
from datetime import timedelta, datetime, timezone
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends
import jwt
from typing import Annotated

from jwt.exceptions import InvalidTokenError

from src.core.config import settings
from src.core.exceptions import CredentialsException
from src.services.user import UserDAO


class AuthServiceABC(ABC):
    @abstractmethod
    def get_password_hash(password: str):
        pass

    @abstractmethod
    def verify_password(plain_password: str, hash_password: str):
        pass

    @abstractmethod
    def authenticate_user(username: str, password: str):
        pass

    @abstractmethod
    def create_access_token(data: dict, expire_delta: timedelta):
        pass

    @abstractmethod
    def get_current_user(token: str):
        pass


class AuthService(AuthServiceABC):

    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

    @staticmethod
    async def create_access_token(
        data: dict,
        expires_delta: timedelta
    ):
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            settings.SECRET_KEY,
            algorithm=settings.ALGORITHM
        )
        return encoded_jwt

    @staticmethod
    async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)]
    ):
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=settings.ALGORITHM
            )
            username = payload.get("sub")
        except InvalidTokenError:
            raise CredentialsException
        user = await UserDAO.find_one_or_none(username=username)
        if not user:
            raise CredentialsException
        return user

    @classmethod
    async def get_password_hash(cls, password: str):
        return cls.pwd_context.hash(password)

    @classmethod
    def verify_password(cls, plain_password: str, hash_password: str):
        return cls.pwd_context.verify(plain_password, hash_password)

    @classmethod
    async def authenticate_user(cls, username: str, password: str):
        user = await UserDAO.find_one_or_none(username=username)
        if not user or not cls.verify_password(
            plain_password=password,
            hash_password=user.hash_password
        ):
            return False
        return user
