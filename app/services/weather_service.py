import httpx
import structlog
from typing import Optional
from datetime import datetime, timedelta

from app.models.weather import WeatherConditions, WeatherRequest
from app.config import settings

logger = structlog.get_logger()


class WeatherServiceError(Exception):
    """Custom exception for weather service errors"""
    pass


class WeatherService:
    def __init__(self):
        self.base_url = settings.weather_api_base_url
        self.timeout = settings.weather_api_timeout
