import os

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


class Settings(BaseSettings):
    # Overall settings for app & database
    app_info: AppSettings = None # type: ignore
    db_info: DatabaseSettings = None # type: ignore

    model_config = SettingsConfigDict(
        env_file=f".env.{env_type}",
        env_file_encoding="utf-8",
        extra="allow", # REVIEW
        validate_assignment=True
    )

    def __init__(self, *args, **kwargs):
        # Opens .env.* file via model_config when Settings() called & reads os system variables
        # Keep *args & **kwargs even though not supplied in Settings() call
        super().__init__(*args, **kwargs)

        # Creates dictionary of all environmental variables in backend-python/
        raw_data = self.__dict__ # REVIEW

        # Sets sub-model values
        self.app_info = AppSettings(**raw_data)
        self.db_info = DatabaseSettings(**raw_data)

def get_settings() -> Settings:
    return Settings()