"""Module for weather conditions model"""

from datetime import datetime
from enum import Enum
from pydantic import BaseModel, Field, ConfigDict


class WeatherClassificationFields(str, Enum):
    """Enum for weather classification fields"""

    TEMPERATURE = "temperature"
    APPARENT_TEMPERATURE = "apparent_temperature"
    HUMIDITY = "humidity"
    WIND_SPEED = "wind_speed"
    PRECIPITATION = "precipitation"
    PRECIPITATION_PROBABILITY = "precipitation_probability"
    CLOUD_COVER = "cloud_cover"
    UV_INDEX = "uv_index"


class WeatherConditions(BaseModel):
    """Represents the weather conditions at a specific point in time."""

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "time": "2025-09-09T13:30:00",
                "weather_code": 3,
                "temperature": 22.5,
                "apparent_temperature": 23.0,
                "humidity": 65.0,
                "wind_speed": 12.0,
                "precipitation": 2.0,
                "precipitation_probability": 15.0,
                "cloud_cover": 40.0,
                "uv_index": 5.2,
                "is_day": True,
            }
        }
    )
    time: datetime = Field(default_factory=datetime.now)
    weather_code: int = Field(
        ...,
        ge=0,
        le=99,
        description="WMO code to describe weather using these standards",
    )

    temperature: float = Field(..., description="Temperature in Celsius")
    apparent_temperature: float = Field(
        ..., description="Apparent temperature in Celsius"
    )
    humidity: float = Field(..., ge=0, le=100, description="Humidity percentage")
    wind_speed: float = Field(..., ge=0, description="Wind speed in km/h")
    precipitation: float = Field(..., ge=0, description="Precipitation in mm")
    precipitation_probability: float = Field(
        ..., ge=0, le=100, description="Precipitation probability percentage"
    )
    cloud_cover: float = Field(..., ge=0, le=100, description="Cloud cover percentage")
    uv_index: float = Field(..., ge=0, description="UV index")
    is_day: bool = Field(..., description="Is day time")
