from typing import Any, Dict
import structlog

from app.schemas.WeatherData import WeatherForecastData, WeatherDailyForecastData
from app.config import settings

from .api_client import WeatherAPIClient
from .cache import WeatherCache
from .models import WeatherDataType, WeatherApiResponse
from .mappers import map_current_weather, map_daily_weather

logger = structlog.get_logger()


class WeatherService:
    CURRENT_PARAMS = ["weather_code", "is_day", "temperature_2m", "apparent_temperature", "relative_humidity_2m",
                      "wind_speed_10m", "precipitation", "precipitation_probability", "cloud_cover", "uv_index", "visibility"]

    DAILY_PARAMS = ["weather_code", "sunrise", "sunset", "sunshine_duration", "temperature_2m_max",
                    "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min",
                    "precipitation_probability_max", "precipitation_hours", "cloud_cover_mean", "uv_index_max"]

    def __init__(self, cache_duration_minutes: int = 30):
        self.api_client = WeatherAPIClient(
            settings.weather_api_base_url,
            settings.weather_api_timeout
        )
        self.cache = WeatherCache(cache_duration_minutes)

    async def get_current_weather(
        self,
        latitude: float,
        longitude: float,
        cache_keys: list[str] = [WeatherDataType.CURRENT]
    ) -> WeatherForecastData:
        """Fetch current weather from Open-Meteo API"""

        logger.info(
            "Fetching current weather data",
            latitude=latitude,
            longitude=longitude
        )

        # Check cache first
        cached_data = self.cache.get(cache_keys, latitude, longitude)
        if cached_data:
            return cached_data

        # Fetch from API
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": self.CURRENT_PARAMS,
            "wind_speed_unit": "kmh",
            "timezone": "auto"
        }

        raw_data = await self.api_client.fetch_weather_data(params)
        weather_data = map_current_weather(raw_data)

        # Cache the result
        self.cache.set(cache_keys, weather_data, latitude, longitude)

        return weather_data

    async def get_daily_weather(
        self,
        latitude: float,
        longitude: float,
        duration_days: int = 3,
        cache_keys: list[str] = [WeatherDataType.DAILY]
    ) -> list[WeatherDailyForecastData]:
        """Fetch daily weather from Open-Meteo API"""

        # Check cache first
        cached_data = self.cache.get(latitude, longitude, cache_keys)
        if cached_data:
            return cached_data

        logger.info(
            "Fetching daily weather data",
            latitude=latitude,
            longitude=longitude
        )

        return []

    def clear_cache(self) -> None:
        """Clear all cached data"""
        self.cache.clear()

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics for monitoring"""
        return self.cache.get_stats()
