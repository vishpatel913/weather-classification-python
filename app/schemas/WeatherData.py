from pydantic import BaseModel, Field
from datetime import datetime

from app.schemas.MetricValue import MetricValue


class WeatherForecastData(BaseModel):
    time: datetime = Field(default_factory=datetime.now)
    weather_code: int = Field(..., ge=0, le=99,
                              description="WMO code to describe weather using these standards")
    is_day: bool = Field(..., description="Is day time")

    temperature: MetricValue[float] = Field(...,
                                            description="Temperature in Celsius")
    temperature_apparent: MetricValue[float] = Field(
        ..., description="Apparent temperature in Celsius")
    humidity: MetricValue[float] = Field(...,
                                         description="Humidity percentage")
    wind_speed: MetricValue[float] = Field(...,
                                           description="Wind speed in km/h")
    precipitation: MetricValue[float] = Field(
        ..., description="Precipitation in mm")
    precipitation_probability: MetricValue[float] = Field(
        ..., description="Precipitation probability percentage")
    cloud_cover: MetricValue[float] = Field(...,
                                            description="Cloud cover percentage")
    uv_index: MetricValue[float] = Field(..., description="UV index"),
