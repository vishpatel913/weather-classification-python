from pydantic import BaseModel, Field
from typing import Optional

# from datetime import datetime

from app.schemas.WeatherData import WeatherForecastData, WeatherDailyForecastData
from app.schemas.api.ResponseBase import ResponseBase


class WeatherRequestParams(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude")
    # duration_hours: Optional[int] = Field(
    #     default=4, ge=1, le=24, description="Request timeline in hours")


class WeatherForecastResponse(WeatherRequestParams, ResponseBase):
    # last_updated: datetime = Field(default_factory=datetime.now)

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
