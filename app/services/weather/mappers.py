from typing import List

import structlog

from app.schemas.WeatherData import WeatherDailyForecastData, WeatherForecastData
from app.utils.metric_transformers import transform_maps_to_metric, transform_maps_to_metric_range

from .exceptions import WeatherAPIFormatError
from .models import WeatherApiResponse

logger = structlog.get_logger()


def map_current_weather(data: WeatherApiResponse) -> WeatherForecastData:
    """Map current weather API response to WeatherForecastData"""
    try:
        current_data = data["current"]
        current_units = data["current_units"]
        current = transform_maps_to_metric(current_data, current_units)
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

    except KeyError as e:
        logger.error(
            "Missing required field in current weather api response", error=str(e))
        raise WeatherAPIFormatError(
            "Invalid current weather data format") from e


def map_daily_weather(data: WeatherApiResponse) -> List[WeatherDailyForecastData]:
    """Map daily weather API response to list of WeatherDailyForecastData"""
    try:
        daily_data = data["daily"]
        daily_units = data["daily_units"]

        total_days = len(daily_data["time"])
        daily_list = []

        for i in range(total_days):
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

    except KeyError as e:
        logger.error(
            "Missing required field in daily weather api response", error=str(e))
        raise WeatherAPIFormatError("Invalid daily weather data format") from e
