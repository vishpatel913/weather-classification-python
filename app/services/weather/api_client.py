"""Weather API client - handles HTTP communication"""

from typing import List, Optional
import httpx
import structlog

from .cache import WeatherCache
from .models import WeatherApiParams, WeatherApiResponse

from .exceptions import WeatherAPITimeoutError, WeatherAPIHTTPError, WeatherServiceError

logger = structlog.get_logger()


class WeatherAPIClient:
    """Handles the actual API communication"""

    def __init__(
        self,
        base_url: str,
        timeout: float,
        cache_duration_minutes: Optional[int] = None,
    ):
        self.base_url = base_url
        self.timeout = timeout
        self.cache = WeatherCache(cache_duration_minutes)

    def _get_cache_key(self, params: WeatherApiParams) -> List[str]:
        cache_keys = [params.get("forecast_days")]
        for weather_type in ["current", "hourly", "daily"]:
            if weather_type in params:
                cache_keys.append(weather_type)
        return cache_keys

    async def fetch_weather_data(self, params: WeatherApiParams) -> WeatherApiResponse:
        """Generic method to fetch weather data from API"""
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.info("Fetching weather data", params=params)

                cache_keys = self._get_cache_key(params)
                cached_data = self.cache.get(
                    cache_keys=cache_keys,
                    latitude=params.get("latitude"),
                    longitude=params.get("longitude"),
                )
                if cached_data:
                    print("----------- Using cached weather data")
                    return cached_data

                response = await client.get(f"{self.base_url}/forecast", params=params)
                print("----------- REQUEST MADE TO WEATHER API")
                response.raise_for_status()
                raw_data = response.json()

                # Cache the raw result
                self.cache.set(
                    cache_keys=cache_keys,
                    data=raw_data,
                    latitude=params.get("latitude"),
                    longitude=params.get("longitude"),
                )
                return raw_data

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
