import logging
import sys

from loguru import logger
from starlette.config import Config
from starlette.datastructures import Secret
from typing import Any, Dict, List, Optional, Union

from app.core.logging import InterceptHandler
from pydantic import AnyHttpUrl, BaseSettings, EmailStr, HttpUrl, PostgresDsn, validator

config = Config(".env")


class Settings(BaseSettings):
    API_PREFIX = "/api"
    VERSION = "0.1.0"
    DEBUG: bool = config("DEBUG", cast=bool, default=False)
    MAX_CONNECTIONS_COUNT: int = config("MAX_CONNECTIONS_COUNT", cast=int, default=10)
    MIN_CONNECTIONS_COUNT: int = config("MIN_CONNECTIONS_COUNT", cast=int, default=10)
    SECRET_KEY: Secret = config("SECRET_KEY", cast=Secret, default="")
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    PROJECT_NAME: str = config("PROJECT_NAME", default="nuntium")
    FIRST_SUPERUSER = 'admin'
    FIRST_SUPERUSER_PASSWORD = '201314'
    # logging configuration
    LOGGING_LEVEL = logging.DEBUG if DEBUG else logging.INFO

    logger.configure(handlers=[{"sink": sys.stderr, "level": LOGGING_LEVEL}])
    logging.basicConfig(
        handlers=[InterceptHandler(level=LOGGING_LEVEL)], level=LOGGING_LEVEL
    )
    MODEL_PATH = config("MODEL_PATH", default="./ml/model/")
    MODEL_NAME = config("MODEL_NAME", default="model.pkl")
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"


settings = Settings()
