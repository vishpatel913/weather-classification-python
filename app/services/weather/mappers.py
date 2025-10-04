from typing import List

import structlog

from app.schemas.weather_data import WeatherDailyForecastData, WeatherForecastData
from app.utils.metric_transformers import (
    transform_maps_to_metric,
    transform_maps_to_metric_range,
)

from .exceptions import WeatherAPIFormatError
from .models import WeatherApiResponse

logger = structlog.get_logger()


def map_current_weather(data: WeatherApiResponse) -> WeatherForecastData:
    """Map current weather API response to WeatherForecastData"""
    try:
        current_data = data["current"]
        current_units = data["current_units"]

        current_metric_data = transform_maps_to_metric(current_data, current_units)
        current_forecast = WeatherForecastData(
            time=current_data["time"],
            weather_code=current_data["weather_code"],
            is_day=current_data["is_day"],
            # Metrics
            temperature=current_metric_data["temperature_2m"],
            apparent_temperature=current_metric_data["apparent_temperature"],
            humidity=current_metric_data["relative_humidity_2m"],
            wind_speed=current_metric_data["wind_speed_10m"],
            precipitation=current_metric_data["precipitation"],
            precipitation_probability=current_metric_data["precipitation_probability"],
            cloud_cover=current_metric_data["cloud_cover"],
            uv_index=current_metric_data["uv_index"],
        )
        return current_forecast

    except KeyError as e:
        logger.error(
            "Missing required field in current weather api response", error=str(e)
        )
        raise WeatherAPIFormatError("Invalid current weather data format") from e


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
                    "apparent_temperature_max": daily_data["apparent_temperature_max"][
                        i
                    ],
                    "apparent_temperature_min": daily_data["apparent_temperature_min"][
                        i
                    ],
                    "uv_index_max": daily_data["uv_index_max"][i],
                    "precipitation_probability_max": daily_data[
                        "precipitation_probability_max"
                    ][i],
                },
                daily_units,
            )

            daily_forecast = WeatherDailyForecastData(
                time=daily_data["time"][i],
                weather_code=daily_data["weather_code"][i],
                sunrise=daily_data["sunrise"][i],
                sunset=daily_data["sunset"][i],
                sunshine_duration=daily_data["sunshine_duration"][i],
                precipitation_hours=daily_data["precipitation_hours"][i],
                # Metrics
                temperature=daily_range_data["temperature_2m"],
                apparent_temperature=daily_range_data["apparent_temperature"],
                precipitation_probability=daily_range_data["precipitation_probability"],
                uv_index=daily_range_data["uv_index"],
            )

            daily_list.append(daily_forecast)

        return daily_list

    except KeyError as e:
        logger.error(
            "Missing required field in daily weather api response", error=str(e)
        )
        raise WeatherAPIFormatError("Invalid daily weather data format") from e


def map_hourly_weather(data: WeatherApiResponse) -> List[WeatherForecastData]:
    """Map daily weather API response to list of WeatherDailyForecastData"""
    try:
        hourly_data = data["hourly"]
        hourly_units = data["hourly_units"]
        total_hours = len(hourly_data["time"])
        hourly_list = []

        for i in range(total_hours):
            hourly_metric_data = transform_maps_to_metric_range(
                {
                    "temperature_2m": hourly_data["temperature_2m"][i],
                    "apparent_temperature": hourly_data["apparent_temperature"][i],
                    "relative_humidity_2m": hourly_data["relative_humidity_2m"][i],
                    "wind_speed_10m": hourly_data["wind_speed_10m"][i],
                    "precipitation": hourly_data["precipitation"][i],
                    "precipitation_probability": hourly_data[
                        "precipitation_probability"
                    ][i],
                    "cloud_cover": hourly_data["cloud_cover"][i],
                    "uv_index": hourly_data["uv_index"][i],
                },
                hourly_units,
            )

            hour_forecast = WeatherForecastData(
                time=hourly_data["time"][i],
                weather_code=hourly_data["weather_code"][i],
                is_day=hourly_data["is_day"][i],
                # Metrics
                temperature=hourly_metric_data["temperature_2m"],
                apparent_temperature=hourly_metric_data["apparent_temperature"],
                humidity=hourly_metric_data["relative_humidity_2m"],
                wind_speed=hourly_metric_data["wind_speed_10m"],
                precipitation=hourly_metric_data["precipitation"],
                precipitation_probability=hourly_metric_data[
                    "precipitation_probability"
                ],
                cloud_cover=hourly_metric_data["cloud_cover"],
                uv_index=hourly_metric_data["uv_index"],
            )

            hourly_list.append(hour_forecast)

        return hourly_list
    except KeyError as e:
        logger.error(
            "Missing required field in hourly weather api response", error=str(e)
        )
        raise WeatherAPIFormatError("Invalid hourly weather data format") from e
