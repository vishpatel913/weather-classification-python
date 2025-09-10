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


@dataclass
class ResponseCacheEntry:
    """Represents a cached weather data entry"""
    timestamp: datetime
    data: Any

    cache_keys: list[str]
    latitude: float
    longitude: float

    def is_expired(self, cache_duration_minutes: int = 30) -> bool:
        """Check if cache entry is expired"""
        expiry_time = self.timestamp + \
            timedelta(minutes=cache_duration_minutes)
        return datetime.now() > expiry_time

    def matches_request(self, cache_keys: list[str], lat: float, lon: float) -> bool:
        """Check if cache entry matches the request parameters"""
        key_match = set(self.cache_keys) == set(cache_keys)
        # Allow small coordinate differences (within ~100m)
        lat_diff = abs(self.latitude - lat) < 0.001
        lon_diff = abs(self.longitude - lon) < 0.001

        return lat_diff and lon_diff and key_match
