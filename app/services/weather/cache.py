"""Weather service caching functionality"""

import structlog
from datetime import datetime
from typing import List, Optional, Any, Dict

from .models import ResponseCacheEntry, WeatherDataType

logger = structlog.get_logger()


class WeatherCache:
    """Manages weather data caching"""

    def __init__(self, cache_duration_minutes: int = 30):
        self.cache: List[ResponseCacheEntry] = []
        self.cache_duration_minutes = cache_duration_minutes

    def get(self, latitude: float, longitude: float,
            data_type: WeatherDataType,
            duration_days: Optional[int] = None) -> Optional[Any]:
        """Retrieve data from cache if available and not expired"""
        for entry in self.cache:
            if (entry.matches_request(latitude, longitude, data_type, duration_days)
                    and not entry.is_expired(self.cache_duration_minutes)):
                logger.info("Cache hit", data_type=data_type.value)
                return entry.data
        return None

    def set(self, data: Any, latitude: float, longitude: float,
            data_type: WeatherDataType,
            duration_days: Optional[int] = None) -> None:
        """Add data to cache"""
        # Remove expired entries and entries for same location/type
        self.cache = [
            entry for entry in self.cache
            if not (entry.is_expired(self.cache_duration_minutes) or
                    entry.matches_request(latitude, longitude, data_type, duration_days))
        ]

        # Add new entry
        entry = ResponseCacheEntry(
            data=data,
            timestamp=datetime.now(),
            latitude=latitude,
            longitude=longitude,
            data_type=data_type,
            duration_days=duration_days
        )
        self.cache.append(entry)
        logger.info("Data cached", data_type=data_type.value,
                    cache_size=len(self.cache))

    def clear(self) -> None:
        """Clear all cached data"""
        self.cache.clear()
        logger.info("Cache cleared")

    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics for monitoring"""
        total_entries = len(self.cache)
        expired_entries = sum(1 for entry in self.cache
                              if entry.is_expired(self.cache_duration_minutes))

        return {
            "total_entries": total_entries,
            "expired_entries": expired_entries,
            "active_entries": total_entries - expired_entries,
            "cache_duration_minutes": self.cache_duration_minutes
        }
