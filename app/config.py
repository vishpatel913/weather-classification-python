from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Literal


class Settings(BaseSettings):
    # Application settings
    app_name: str = Field(default="Weather Clothing Service")
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

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()
