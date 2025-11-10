"""Schema definitions for weather response."""

from typing import Optional
from pydantic import BaseModel, Field

from app.schemas.weather_data import WeatherForecastData, WeatherDailyForecastData
from app.schemas.api.response_base import ResponseBase


class WeatherRequestParams(BaseModel):
    """Schema for the request parameters of weather routes"""

    latitude: float = Field(..., ge=-90, le=90, description="Latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude")
    forecast_length: Optional[int] = Field(
        default=3, ge=1, le=16, description="Request timeline in days (1, 3, 7, 14, 16)"
    )


class WeatherForecastResponse(WeatherRequestParams, ResponseBase):
    """Schema for the response from weather routes"""

    current: Optional[WeatherForecastData] = Field(
        None, description="Current forecast for requested coords"
    )
    today: Optional[WeatherDailyForecastData] = Field(
        None, description="Today's daily forecast for requested coords"
    )
    hourly: Optional[list[WeatherForecastData]] = Field(
        None, description="Hourly forecast for requested coords"
    )
    daily: Optional[list[WeatherDailyForecastData]] = Field(
        None, description="Daily forecast for requested coords"
    )
