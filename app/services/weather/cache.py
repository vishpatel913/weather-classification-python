"""Weather service caching functionality"""

import structlog
from datetime import datetime
from typing import List, Optional, Any, Dict

from .models import ResponseCacheEntry

logger = structlog.get_logger()


class WeatherCache:
    """Manages weather data caching"""

    def __init__(self, cache_duration_minutes: int = 30):
        self.store: List[ResponseCacheEntry] = []
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
        entry = ResponseCacheEntry(
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
