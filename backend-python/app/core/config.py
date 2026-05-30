import os
from typing import Optional

from pydantic import BaseModel, SecretStr, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


env_type = os.getenv("ENV", "development")


class AppSettings(BaseModel):
    # General app information
    env: str
    app_name: str
    app_version: str
    debug: bool = True
    log_level: str


class DatabaseSettings(BaseModel):
    # Database connection information
    db_user: str
    db_password: SecretStr
    db_host: str
    db_port: int = 5432
    db_name: str

    @computed_field
    def db_url(self) -> str:
        return (
            f"postgresql://{self.db_user}:{self.db_password.get_secret_value()}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


class AWSSettings(BaseModel):
    # AWS credentials + region information for production environment
    # Set defaults to initialize empty instance for development environment
    access_key_id: Optional[str] = None
    secret_access_key: Optional[SecretStr] = None  
    default_region: str = "us-east-1"


class Settings(BaseSettings):
    # Pydantic generates fields directly from environmental variables
    app_info: AppSettings
    db_info: DatabaseSettings
    aws_info: AWSSettings = AWSSettings()

    model_config = SettingsConfigDict(
        env_file=f".env.{env_type}",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",
        extra="forbid",
        validate_assignment=True
    )


def get_settings() -> Settings:
    return Settings()