"""Weather service data models and enums"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Optional, TypedDict, Dict, List


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
