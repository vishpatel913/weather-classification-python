from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
import datetime


class WeatherConditions(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "temperature": 22.5,
                "temperature_feels_like": 23.0,
                "humidity": 65.0,
                "wind_speed": 12.0,
                "precipitation_chance": 15.0,
                "precipitation": 2.0,
                "cloud_cover": 40.0,
                "uv_index": 5.2
            }
        }
    )

    temperature: float = Field(..., description="Temperature in Celsius")
    temperature_feels_like: float = Field(...,
                                          description="Apparent temperature in Celsius")
    humidity: float = Field(..., ge=0, le=100,
                            description="Humidity percentage")
    wind_speed: float = Field(..., ge=0, description="Wind speed in km/h")
    precipitation: float = Field(..., ge=0, description="Precipitation in mm")
    precipitation_chance: float = Field(..., ge=0, le=100,
                                        description="Precipitation chance percentage")
    cloud_cover: float = Field(..., ge=0, le=100,
                               description="Cloud cover percentage")
    uv_index: Optional[float] = Field(None, ge=0, description="UV index")
    timestamp: datetime = Field(default_factory=datetime.now)


class WeatherRequest(BaseModel):
    latitude: float = Field(..., ge=-90, le=90, description="Latitude")
    longitude: float = Field(..., ge=-180, le=180, description="Longitude")
    duration_hours: int = Field(
        default=4, ge=1, le=24, description="Hours ahead")
