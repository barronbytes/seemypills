import os
from typing import Optional

from pydantic import BaseModel, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


env_type = os.getenv("ENV", "development")


class AppSettings(BaseModel):
    """ General app information"""
    ENV: str
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool = True
    LOG_LEVEL: str


class CorsSettings(BaseModel):
    """Cross-origin resource sharing allow-list for the frontend's origin(s)"""
    ALLOWED_ORIGINS: list[str]


class DatabaseSettings(BaseModel):
    """Database connection information"""
    DB_USER: str
    DB_PASSWORD: SecretStr
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str

    @computed_field
    def db_url(self) -> str:
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD.get_secret_value()}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )


class AWSSettings(BaseModel):
    """
    AWS credentials + region information for production environment
    Set defaults to initialize empty instance for development environment
    """
    ACCESS_KEY_ID: Optional[str] = None
    SECRET_ACCESS_KEY: Optional[SecretStr] = None
    DEFAULT_REGION: str = "us-east-1"


class Settings(BaseSettings):
    """Pydantic generates fields directly from environmental variables"""
    app_info: AppSettings
    cors_info: CorsSettings
    db_info: DatabaseSettings
    aws_info: AWSSettings = AWSSettings()

    model_config = SettingsConfigDict(
        env_file=f".env.{env_type}",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="forbid",
        validate_assignment=True,
        case_sensitive=False
    )


def get_settings() -> Settings:
    """Returns Settings class instance"""
    return Settings()