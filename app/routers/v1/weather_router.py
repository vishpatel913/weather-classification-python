"""Weather Router module for handling weather-related API endpoints."""

from typing import Annotated
from fastapi import APIRouter, Depends, Query
import structlog

from app.schemas.api.weather_response import (
    WeatherRequestParams,
    WeatherForecastResponse,
)
from app.services.weather import WeatherService

logger = structlog.get_logger()

WeatherRouter = APIRouter(prefix="/v1/weather", tags=["weather"])


async def get_weather_params(
    latitude: Annotated[float, Query(..., ge=-90, le=90)],
    longitude: Annotated[float, Query(..., ge=-180, le=180)],
):
    """Extracts and returns weather request parameters from query."""
    return WeatherRequestParams(latitude=latitude, longitude=longitude)


def get_weather_service():
    """Creates and returns an instance of WeatherService as a dependency."""
    return WeatherService(cache_duration_minutes=10)


@WeatherRouter.get("/current", response_model=WeatherForecastResponse)
async def get_current_forecast(
    query: Annotated[WeatherRequestParams, Depends(get_weather_params)],
    weather_service: WeatherService = Depends(get_weather_service),
):
    """Handler for getting current weather conditions"""
    logger.info("Requesting current weather...")

    current = await weather_service.get_current_weather(
        latitude=query.latitude,
        longitude=query.longitude,
    )
    daily = await weather_service.get_daily_weather(
        latitude=query.latitude,
        longitude=query.longitude,
    )

    logger.info("Requested current weather")

    return WeatherForecastResponse(
        latitude=query.latitude,
        longitude=query.longitude,
        current=current,
        today=daily[0],
    )


@WeatherRouter.get("/hourly", response_model=WeatherForecastResponse)
async def get_hourly_forecast(
    query: Annotated[WeatherRequestParams, Depends(get_weather_params)],
    weather_service: WeatherService = Depends(get_weather_service),
):
    """Handler for getting hourly weather conditions"""
    logger.info("Requesting hourly weather...")
    hourly = await weather_service.get_hourly_weather(
        latitude=query.latitude,
        longitude=query.longitude,
        forecast_length=query.forecast_length,
    )

    logger.info("Requested hourly weather")

    return WeatherForecastResponse(
        latitude=query.latitude,
        longitude=query.longitude,
        forecast_length=query.forecast_length,
        hourly=hourly,
    )
