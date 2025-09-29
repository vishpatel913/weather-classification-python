"""Weather service data models and enums"""

from enum import Enum
from typing import Optional, TypedDict, Dict, List


class WeatherDataType(Enum):
    CURRENT = "current"
    DAILY = "daily"
    HOURLY = "hourly"


WeatherApiResponseValue = str | int | float


class WeatherApiResponse(TypedDict):
    latitude: float
    longitude: float
    generationtime_ms: float
    utc_offset_seconds: int
    timezone: str
    timezone_abbreviation: str
    elevation: float
    current: Optional[Dict[str, WeatherApiResponseValue]]
    hourly: Optional[List[WeatherApiResponseValue]]
    daily: Optional[List[WeatherApiResponseValue]]
    current_units: Optional[Dict[str, str]]
    hourly_units: Optional[Dict[str, str]]
    daily_units: Optional[Dict[str, str]]


class WeatherApiParams(TypedDict):
    latitude: float
    longitude: float

    current: Optional[List[str]]
    daily: Optional[List[str]]
    hourly: Optional[List[str]]

    timezone: str = "auto"
    forecast_days: Optional[int] = 3
    wind_speed_unit: Optional[str] = "kmh"
    temperature_unit: Optional[str] = "celsius"
    precipitation_unit: Optional[str] = "mm"
