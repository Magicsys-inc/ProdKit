import os

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

    # Password
    PEPPER_SECRET: str | bytes = "super secret pepper"
    SALT_SECRET: bytes | None = None  # Argon2 handles salt! Use custom salt carefully

    # JWK
    SECRET: str = "super secret jwt secret"
    # JWKS: JWKSFile = Field(default="./.jwks.json")  # TODO: config it based on multi-tenancy
    CURRENT_JWK_KID: str = f"{get_app_name}_dev"
    WWW_AUTHENTICATE_REALM: str = f"{get_app_name}"

    model_config = SettingsConfigDict(
        env_prefix=f"{get_app_name}_",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_file=env_file,
        extra="allow",
    )

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


settings = Settings()
