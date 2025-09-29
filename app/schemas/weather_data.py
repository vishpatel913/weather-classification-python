from datetime import datetime
from pydantic import BaseModel, Field

from app.schemas.metric_value import MetricValue, MetricRangeValue


class WeatherForecastBase(BaseModel):
    time: datetime = Field(default_factory=datetime.now)
    weather_code: int = Field(
        ...,
        ge=0,
        le=99,
        description="WMO code to describe weather using these standards",
    )


class WeatherForecastData(WeatherForecastBase):
    is_day: bool = Field(..., description="Is day time")

    temperature: MetricValue[float] = Field(..., description="Temperature in Celsius")
    apparent_temperature: MetricValue[float] = Field(
        ..., description="Apparent temperature in Celsius"
    )
    humidity: MetricValue[float] = Field(..., description="Humidity percentage")
    wind_speed: MetricValue[float] = Field(..., description="Wind speed in km/h")
    precipitation: MetricValue[float] = Field(..., description="Precipitation in mm")
    precipitation_probability: MetricValue[float] = Field(
        ..., description="Precipitation probability percentage"
    )
    cloud_cover: MetricValue[float] = Field(..., description="Cloud cover percentage")
    uv_index: MetricValue[float] = Field(..., description="UV index")


class WeatherDailyForecastData(WeatherForecastBase):
    sunrise: datetime = Field(..., description="Time of sun rise")
    sunset: datetime = Field(..., description="Time of sun set")
    sunshine_duration: float = Field(
        ..., description="Amount of time the sun will be out"
    )

    temperature: MetricRangeValue[float] = Field(
        ..., description="Temperature range in Celsius"
    )
    apparent_temperature: MetricRangeValue[float] = Field(
        ..., description="Apparent temperature range in Celsius"
    )
    precipitation_probability: MetricRangeValue[float] = Field(
        ..., description="Precipitation probability range"
    )
    precipitation_hours: float = Field(
        ..., description="Hours of precipitation in the day"
    )
    uv_index: MetricRangeValue[float] = Field(..., description="UV index")
