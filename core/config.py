import secrets
from typing import List, Optional

from pydantic import BaseSettings, HttpUrl, validator


class Settings(BaseSettings):

    PROJECT_NAME: str = "My Ferm"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    SERVER_HOST: str = "localhost"
    SERVER_PORT: str = "8012"
    HOST_URI: str = f"http://{SERVER_HOST}:{SERVER_PORT}"
    API_PREFIX: str = "/api/v1"
    SQLALCHEMY_DATABASE_URI: str = "postgresql://postgres:1234@localhost:5432/myferm"
    REDIS_URI: str = "redis://redis:6379"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    FIRST_ADMIN_USERNAME: str = "admin"
    FIRST_ADMIN_PASSWORD: str = "admin"

    ENV_NAME: str = "development"
    MEDIA_DIR: str = "/media/"

    class Config:
        case_sensitive = True


settings = Settings()
