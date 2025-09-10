import httpx
import structlog

from app.schemas.WeatherData import WeatherForecastData, WeatherDailyForecastData
from app.utils.metric_transformers import transform_maps_to_metric, transform_maps_to_metric_range
from app.config import settings

logger = structlog.get_logger()

current_params = ["weather_code", "is_day", "temperature_2m", "apparent_temperature", "relative_humidity_2m",
                  "wind_speed_10m", "precipitation", "precipitation_probability", "cloud_cover", "uv_index", "visibility"]
daily_params = ["weather_code", "sunrise", "sunset", "sunshine_duration", "temperature_2m_max",
                "temperature_2m_min", "apparent_temperature_max", "apparent_temperature_min",
                "precipitation_probability_max", "precipitation_hours", "cloud_cover_mean", "uv_index_max"]


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
    ) -> WeatherForecastData:
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
                    "Fetching current weather data",
                    latitude=latitude,
                    longitude=longitude
                )

                response = await client.get(
                    f"{self.base_url}/forecast",
                    params=params
                )
                response.raise_for_status()
                data = response.json()

                current = transform_maps_to_metric(
                    data["current"], data["current_units"])

                return WeatherForecastData(
                    time=current["time"]["value"],
                    weather_code=current["weather_code"]["value"],
                    is_day=current["is_day"]["value"],
                    temperature=current["temperature_2m"],
                    temperature_apparent=current["apparent_temperature"],
                    humidity=current["relative_humidity_2m"],
                    wind_speed=current["wind_speed_10m"],
                    precipitation=current["precipitation"],
                    precipitation_probability=current["precipitation_probability"],
                    cloud_cover=current["cloud_cover"],
                    uv_index=current["uv_index"],
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

    async def get_daily_weather(
        self,
        latitude: float,
        longitude: float,
        duration_days: int = 3
    ) -> list[WeatherDailyForecastData]:
        """Fetch daily weather from Open-Meteo API"""

        params = {
            "latitude": latitude,
            "longitude": longitude,
            "forecast_days": duration_days,
            "daily": daily_params,
            "wind_speed_unit": "kmh",
            "timezone": "auto"
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                logger.info(
                    "Fetching daily weather data",
                    latitude=latitude,
                    longitude=longitude
                )

                response = await client.get(
                    f"{self.base_url}/forecast",
                    params=params
                )
                response.raise_for_status()
                data = response.json()

                daily_units = data["daily_units"]
                daily_data = data["daily"]
                daily_list = []

                for i in range(duration_days):
                    daily_range_data = transform_maps_to_metric_range(
                        {
                            "temperature_2m_max": daily_data["temperature_2m_max"][i],
                            "temperature_2m_min": daily_data["temperature_2m_min"][i],
                            "apparent_temperature_max": daily_data["apparent_temperature_max"][i],
                            "apparent_temperature_min": daily_data["apparent_temperature_min"][i],
                            "uv_index_max": daily_data["uv_index_max"][i],
                            "precipitation_probability_max": daily_data["precipitation_probability_max"][i],
                        }, daily_units)

                    daily_forecast = WeatherDailyForecastData(
                        time=daily_data["time"][i],
                        weather_code=daily_data["weather_code"][i],
                        sunrise=daily_data["sunrise"][i],
                        sunset=daily_data["sunset"][i],
                        sunshine_duration=daily_data["sunshine_duration"][i],
                        precipitation_hours=daily_data["precipitation_hours"][i],

                        temperature=daily_range_data["temperature_2m"],
                        temperature_apparent=daily_range_data["apparent_temperature"],
                        precipitation_probability=daily_range_data["precipitation_probability"],
                        uv_index=daily_range_data["uv_index"],
                    )

                    daily_list.append(daily_forecast)

                return daily_list

        except httpx.TimeoutException as e:
            logger.error("Weather API timeout", error=str(e))
            raise WeatherServiceError(
                "Weather service timeout") from e
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
