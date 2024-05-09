from pydantic import PostgresDsn, RedisDsn, SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_title: str
    app_description: str
    app_version: str

    secret_key: SecretStr
    algorithm: str
    access_token_expire_minutes: int

    postgres_uri: PostgresDsn
    redis_uri: RedisDsn

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
