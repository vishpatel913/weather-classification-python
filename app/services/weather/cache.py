"""Weather service caching functionality"""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional, Any, Dict

import structlog

logger = structlog.get_logger()


@dataclass
class WeatherCacheEntry:
    """Represents a cached weather entry and data"""

    timestamp: datetime
    data: Any

    cache_keys: list[str]
    latitude: float
    longitude: float

    def is_expired(self, cache_duration_minutes: int = 30) -> bool:
        """Check if cache entry is expired"""
        expiry_time = self.timestamp + timedelta(minutes=cache_duration_minutes)
        return datetime.now() > expiry_time

    def matches_request(self, cache_keys: list[str], lat: float, lon: float) -> bool:
        """Check if cache entry matches the request parameters"""
        key_match = set(self.cache_keys) == set(cache_keys)
        # Allow small coordinate differences (within ~100m)
        lat_diff = abs(self.latitude - lat) < 0.001
        lon_diff = abs(self.longitude - lon) < 0.001

        return lat_diff and lon_diff and key_match


class WeatherCache:
    """Manages weather data caching"""

    def __init__(self, cache_duration_minutes: int = 30):
        self.store: List[WeatherCacheEntry] = []
        self.cache_duration_minutes = cache_duration_minutes

    def get(
        self, cache_keys: list[str], latitude: float, longitude: float
    ) -> Optional[Any]:
        """Retrieve data from cache if available and not expired"""
        for entry in self.store:
            if entry.matches_request(
                cache_keys, latitude, longitude
            ) and not entry.is_expired(self.cache_duration_minutes):
                logger.info("Cache hit", cache_keys="".join(str(x) for x in cache_keys))
                return entry.data
        return None

    def set(
        self, cache_keys: list[str], data: Any, latitude: float, longitude: float
    ) -> None:
        """Add data to cache"""
        # Remove expired entries and entries for same location/type
        self.store = [
            entry
            for entry in self.store
            if not (
                entry.is_expired(self.cache_duration_minutes)
                or entry.matches_request(cache_keys, latitude, longitude)
            )
        ]

        # Add new entry
        entry = WeatherCacheEntry(
            data=data,
            timestamp=datetime.now(),
            latitude=latitude,
            longitude=longitude,
            cache_keys=cache_keys,
        )
        self.store.append(entry)
        logger.info(
            "Data cached",
            cache_keys="".join(str(x) for x in cache_keys),
            cache_size=len(self.store),
        )

    def clear(self) -> None:
        """Clear all cached data"""
        self.store.clear()
        logger.info("Cache cleared")

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics for monitoring"""
        total_entries = len(self.store)
        expired_entries = sum(
            1 for entry in self.store if entry.is_expired(self.cache_duration_minutes)
        )

        return {
            "total_entries": total_entries,
            "expired_entries": expired_entries,
            "active_entries": total_entries - expired_entries,
            "cache_duration_minutes": self.cache_duration_minutes,
        }
