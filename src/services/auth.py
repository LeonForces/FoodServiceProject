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
    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    def create_access_token(
        data: dict,
        expires_delta: timedelta | None = timedelta(minutes=15)
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

    async def get_current_user(
            self,
            token: Annotated[str, Depends(oauth2_scheme)]):
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

    def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password: str, hash_password: str):
        return self.pwd_context.verify(plain_password, hash_password)

    async def authenticate_user(self, username: str, password: str):
        user = await UserDAO.find_one_or_none(username=username)
        if not user or not self.verify_password(
            plain_password=password,
            hash_password=user.hash_password
        ):
            return False
        return user
