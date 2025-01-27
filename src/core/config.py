from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):

    model_config = SettingsConfigDict(env_file="../.env")
    DB_HOST: str = Field(
        "localhost",
        env="DB_HOST"
    )
    DB_PORT: str = Field(
        "5432",
        env="DB_PORT"
    )
    DB_NAME: str = Field(
        "test",
        env="DB_NAME"
    )
    DB_USER: str = Field(
        "postgres",
        env="DB_USER"
    )
    DB_PASSWORD: str = Field(
        "1234",
        env="DB_PASSWORD"
    )

    @property
    def db_url(self):
        return "postgres+asyncpg://" + \
            f"{self.DB_USER}:{self.DB_PASSWORD}@" + \
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
