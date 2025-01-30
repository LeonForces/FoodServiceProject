from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file="../.env")
    POSTGRES_HOST: str = Field(
        "localhost",
        env="POSTGRES_HOST"
    )
    POSTGRES_PORT: str = Field(
        "5432",
        env="POSTGRES_PORT"
    )
    POSTGRES_DB: str = Field(
        env="POSTGRES_DB"
    )
    POSTGRES_USER: str = Field(
        "postgres",
        env="POSTGRES_USER"
    )
    POSTGRES_PASSWORD: str = Field(
        "1234",
        env="POSTGRES_PASSWORD"
    )
    echo: bool = Field(
        True,
        env="ECHO"
    )

    SECRET_KEY: str = Field(
        env="SECRET_KEY"
    )
    ALGORITHM: str = Field(
        "HS256",
        env="ALGORITHM"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        15,
        env="ACCESS_TOKEN_EXPIRE_MINUTES"
    )
    COOKIE_MAX_AGE: int = Field(
        env="COOKIE_MAX_AGE"
    )

    @property
    def db_url(self):
        return "postgresql+asyncpg://" + \
            f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@" + \
            f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


settings = Settings()
