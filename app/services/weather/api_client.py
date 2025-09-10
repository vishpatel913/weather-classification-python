"""Weather API client - handles HTTP communication"""

import httpx
import structlog
from typing import Dict, Any

from app.services.weather.models import WeatherApiResponse

from .exceptions import WeatherAPITimeoutError, WeatherAPIHTTPError, WeatherServiceError

logger = structlog.get_logger()


class WeatherAPIClient:
    """Handles the actual API communication"""

    def __init__(self, base_url: str, timeout: float):
        self.base_url = base_url
        self.timeout = timeout

    async def fetch_weather_data(self, params: Dict[str, Any]) -> WeatherApiResponse:
        """Generic method to fetch weather data from API"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.info("Fetching weather data", params=params)

                response = await client.get(f"{self.base_url}/forecast", params=params)
                response.raise_for_status()
                return response.json()

        except httpx.TimeoutException as e:
            logger.error("Weather API timeout", error=str(e))
            raise WeatherAPITimeoutError("Weather service timeout") from e

        except httpx.HTTPStatusError as e:
            logger.error(
                "Weather API HTTP error",
                status_code=e.response.status_code,
                error=str(e),
            )
            raise WeatherAPIHTTPError(
                f"Weather API error: {e.response.status_code}", e.response.status_code
            ) from e

        except Exception as e:
            logger.error("Unexpected weather API error", error=str(e))
            raise WeatherServiceError("Weather service unavailable") from e
