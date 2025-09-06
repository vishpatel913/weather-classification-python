from typing import Optional
import httpx
import structlog

from app.schemas.Weather import WeatherConditions
from app.config import settings

logger = structlog.get_logger()

current_params = ["weather_code", "is_day", "temperature_2m", "apparent_temperature", "relative_humidity_2m", "wind_speed_10m",
                  "precipitation", "precipitation_probability", "cloud_cover", "uv_index", "visibility"]
daily_params = ["weather_code", "sunrise", "sunset", "temperature_2m_max", "temperature_2m_min", "apparent_temperature_max",
                "apparent_temperature_min", "precipitation_probability_max", "daylight_duration", "sunshine_duration", "uv_index_max"]


class WeatherServiceError(Exception):
    """Custom exception for weather service errors"""
    pass


class WeatherService:
    def __init__(self):
        self.base_url = settings.weather_api_base_url
        self.timeout = settings.weather_api_timeout

    async def get_current_weather(
        self,
        latitude: float,
        longitude: float,
        duration: Optional[int] = 4
    ) -> WeatherConditions:
        """Fetch current weather from Open-Meteo API"""

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": current_params,
            "wind_speed_unit": "kmh",
            "timezone": "auto"
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.info(
                    "Fetching weather data",
                    latitude=latitude,
                    longitude=longitude
                )

                response = await client.get(
                    f"{self.base_url}/forecast",
                    params=params
                )
                response.raise_for_status()
                data = response.json()

                current = data["current"]

                return WeatherConditions(
                    time=current["time"],
                    weather_code=current["weather_code"],
                    temperature=current["temperature_2m"],
                    temperature_apparent=current["apparent_temperature"],
                    humidity=current["relative_humidity_2m"],
                    wind_speed=current["wind_speed_10m"],
                    precipitation=current["precipitation"],
                    precipitation_probability=current["precipitation_probability"],
                    cloud_cover=current["cloud_cover"],
                    uv_index=current["uv_index"],
                    is_day=current["is_day"],
                )

        except httpx.TimeoutException as e:
            logger.error("Weather API timeout", error=str(e))
            raise WeatherServiceError("Weather service timeout") from e
        except httpx.HTTPStatusError as e:
            logger.error(
                "Weather API HTTP error",
                status_code=e.response.status_code,
                error=str(e)
            )
            raise WeatherServiceError(
                f"Weather API error: {e.response.status_code}") from e
        except KeyError as e:
            logger.error(
                "Unexpected weather API response format", error=str(e))
            raise WeatherServiceError("Invalid weather data format") from e
        except Exception as e:
            logger.error("Unexpected weather service error", error=str(e))
            raise WeatherServiceError("Weather service unavailable") from e
