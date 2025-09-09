from fastapi import APIRouter, Depends, Query
from typing import Annotated
import structlog

from app.schemas.Weather import (
    WeatherRequestParams,
    WeatherConditions,
)
from app.services.WeatherService import WeatherService

logger = structlog.get_logger()

WeatherRouter = APIRouter(
    prefix="/v1/weather", tags=["weather"]
)


async def get_weather_params(
    latitude: Annotated[float, Query(..., ge=-90, le=90)],
    longitude: Annotated[float, Query(..., ge=-180, le=180)],

):
    return WeatherRequestParams(latitude=latitude, longitude=longitude)


@WeatherRouter.get("/current", response_model=WeatherConditions)
async def get_current(
    query: Annotated[WeatherRequestParams, Depends(get_weather_params)],
    weather_service: WeatherService = Depends()
):
    """Handler for getting current weather conditions"""
    logger.info("Requesting current weather...")
    current = await weather_service.get_current_weather(latitude=query.latitude, longitude=query.longitude, )
    logger.info("Requested current weather")
    return current
