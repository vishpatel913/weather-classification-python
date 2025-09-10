"""Weather service caching functionality"""

import structlog
from datetime import datetime
from typing import List, Optional, Any, Dict

from .models import ResponseCacheEntry

logger = structlog.get_logger()


class WeatherCache:
    """Manages weather data caching"""

    def __init__(self, cache_duration_minutes: int = 30):
        self.cache: List[ResponseCacheEntry] = []
        self.cache_duration_minutes = cache_duration_minutes

    def get(self, cache_key: str, latitude: float, longitude: float) -> Optional[Any]:
        """Retrieve data from cache if available and not expired"""
        for entry in self.cache:
            if (entry.matches_request(cache_key, latitude, longitude)
                    and not entry.is_expired(self.cache_duration_minutes)):
                logger.info("Cache hit", cache_key=cache_key.value)
                return entry.data
        return None

    def set(self, cache_key: str, data: Any, latitude: float, longitude: float) -> None:
        """Add data to cache"""
        # Remove expired entries and entries for same location/type
        self.cache = [
            entry for entry in self.cache
            if not (entry.is_expired(self.cache_duration_minutes) or
                    entry.matches_request(cache_key, latitude, longitude))
        ]

        # Add new entry
        entry = ResponseCacheEntry(
            data=data,
            timestamp=datetime.now(),
            latitude=latitude,
            longitude=longitude,
            cache_key=cache_key,
        )
        self.cache.append(entry)
        logger.info("Data cached", cache_key=cache_key.value,
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
