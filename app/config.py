from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal


class Settings(BaseSettings):
    # Application settings
    app_name: str = Field(default="Weather Classification Service")
    app_version: str = Field(default="0.1.0")
    debug: bool = Field(default=False)
    host: str = Field(default="0.0.0.0")
    port: int = Field(default=8080)
    log_level: Literal["DEBUG", "INFO", "WARNING",
                       "ERROR"] = Field(default="INFO")

    # Weather API settings
    weather_api_base_url: str = Field(default="https://api.open-meteo.com/v1")
    weather_api_timeout: int = Field(default=30)

    # Health check settings
    health_check_timeout: int = Field(default=5)

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False
    )


settings = Settings()
