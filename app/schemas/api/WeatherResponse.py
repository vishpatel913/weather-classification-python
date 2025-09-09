from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime

from app.schemas.WeatherData import WeatherForecastData
from app.schemas.api.ResponseBase import ResponseBase


class WeatherRequestParams(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude")
    duration_hours: Optional[int] = Field(
        default=4, ge=1, le=24, description="Request timeline in hours")


class WeatherForecastResponse(ResponseBase):
    latitude: float = Field(..., ge=-90, le=90, description="Latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude")
    # last_updated: datetime = Field(default_factory=datetime.now)
    current: Optional[WeatherForecastData] = Field(...,
                                                   description="Current forecast for requested coords")
