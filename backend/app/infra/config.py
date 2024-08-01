import os
from typing import Literal

from pydantic import (
    PostgresDsn,
)
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.infra.kit.enums import Environment

# from app.infra.kit.jwk import JWKSFile

env = Environment(os.getenv("PRODKIT_ENV", Environment.DEVELOPMENT))
env_file = ".env.testing" if env == Environment.TESTING else ".env"


class Settings(BaseSettings):
    """
    Environment variables will always take priority over values loaded from a dotenv file
    https://docs.pydantic.dev/latest/concepts/pydantic_settings
    """

    ENV: Environment = Environment.DEVELOPMENT
    DEBUG: bool = False
    LOG_LEVEL: str = "DEBUG"
    TESTING: bool = False

    ORGANIZATION: str = "ProdKit"
    APP_NAME: str = "ProdKit"
    APP_URL: str = "prodkit.dev"

    @classmethod
    def get_app_name(cls) -> str:
        return cls.APP_NAME.lower()

    @property
    def app_name(self) -> str:
        return self.APP_NAME.lower()

    # Application behaviours
    API_PAGINATION_MAX_LIMIT: int = 100

    # JSON list of accepted CORS origins
    CORS_ORIGINS: list[str] = []

    ALLOWED_HOSTS: set[str] = {"127.0.0.1:3000", "localhost:3000"}

    # Base URL for the backend. Used by generate_external_url to
    # generate URLs to the backend accessible from the outside.
    BASE_URL: str = "http://127.0.0.1:8000/api/v1"

    # URL to frontend app.
    # Update to ngrok domain or similar in case you want
    # working Github badges in development.
    FRONTEND_BASE_URL: str = "http://127.0.0.1:3000"
    FRONTEND_DEFAULT_RETURN_PATH: str = "/feed"

    # Password
    PEPPER_SECRET: str | bytes = "super secret pepper"
    SALT_SECRET: bytes | None = None  # Argon2 handles salt! Use custom salt carefully

    # JWK
    SECRET: str = "super secret jwt secret"
    # JWKS: JWKSFile = Field(default="./.jwks.json")  # TODO: config it based on multi-tenancy
    CURRENT_JWK_KID: str = f"{get_app_name}_dev"
    WWW_AUTHENTICATE_REALM: str = f"{get_app_name}"

    # Database
    POSTGRES_USER: str = f"{get_app_name}"
    POSTGRES_PWD: str = f"{get_app_name}"
    POSTGRES_HOST: str = "127.0.0.1"
    POSTGRES_PORT: int = 5432
    POSTGRES_DATABASE: str = f"{get_app_name}_development"
    DATABASE_POOL_SIZE: int = 5
    DATABASE_SYNC_POOL_SIZE: int = 1  # Specific pool size for sync connection: since we only use it in OAuth2 router, don't waste resources.
    DATABASE_POOL_RECYCLE_SECONDS: int = 600  # 10 minutes

    SPECIAL_SCHEMA: str = "special"
    TENANT_SCHEMA: str = "tenant_{}"

    # Redis
    REDIS_HOST: str = "127.0.0.1"
    REDIS_PORT: int = 6379
    # REDIS_DB_NUMBER: int = 0
    # REDIS_PASSWORD: str = "secret"

    DEFAULT_QUEUE_NAME: str = "arq:queue"

    model_config = SettingsConfigDict(
        env_prefix=f"{get_app_name}_",
        env_file_encoding="utf-8",
        case_sensitive=True,
        env_file=env_file,
        extra="allow",
    )

    @property
    def redis_url(self) -> str:
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}"

    def get_postgres_dsn(
        self, schema_name: str | None, driver: Literal["asyncpg", "psycopg2"]
    ) -> str:
        base_dsn: str = PostgresDsn.build(  # type: ignore
            scheme=f"postgresql+{driver}",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PWD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DATABASE,
        )
        return f"{base_dsn}/{schema_name}" if schema_name else base_dsn

    def is_environment(self, environment: Environment) -> bool:
        return environment == self.ENV

    def is_development(self) -> bool:
        return self.is_environment(Environment.DEVELOPMENT)

    def is_testing(self) -> bool:
        return self.is_environment(Environment.TESTING)

    def is_staging(self) -> bool:
        return self.is_environment(Environment.STAGING)

    def is_production(self) -> bool:
        return self.is_environment(Environment.PRODUCTION)

    def generate_external_url(self, path: str) -> str:
        return f"{self.BASE_URL}{path}"

    def generate_frontend_url(self, path: str) -> str:
        return f"{self.FRONTEND_BASE_URL}{path}"


settings = Settings()
