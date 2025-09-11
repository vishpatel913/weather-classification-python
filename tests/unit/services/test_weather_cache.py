"""Unit tests for WeatherCache and dataclass"""

from datetime import datetime, timedelta
import pytest

from app.services.weather.cache import WeatherCache, WeatherCacheEntry


@pytest.fixture(name="weather_cache")
def fixture_weather_cache():
    """Provides a fresh WeatherCache instance for each test."""
    return WeatherCache(cache_duration_minutes=30)


def test_initialization(weather_cache):
    """Test that the cache is initialized correctly."""
    assert len(weather_cache.store) == 0
    assert weather_cache.cache_duration_minutes == 30


def test_set_and_get_cache_hit(weather_cache):
    """Test that data can be set and then retrieved."""
    # Arrange
    cache_keys = ["temperature"]
    data = {"value": 25.0}
    lat, lon = 51.5074, -0.1278

    # Act
    weather_cache.set(cache_keys, data, lat, lon)
    retrieved_data = weather_cache.get(cache_keys, lat, lon)

    # Assert
    assert retrieved_data is not None
    assert retrieved_data == data


def test_get_cache_miss(weather_cache):
    """Test that get() returns None for a cache miss."""
    # Arrange
    cache_keys = ["temperature"]
    lat, lon = 51.5074, -0.1278

    # Act
    retrieved_data = weather_cache.get(cache_keys, lat, lon)

    # Assert
    assert retrieved_data is None


# def test_get_expired_entry(weather_cache, mock_datetime_now):
#     """Test that an expired entry is not returned."""
#     # Arrange
#     cache_keys = ["temperature"]
#     data = {"value": 25.0}
#     lat, lon = 51.5074, -0.1278

#     weather_cache.set(cache_keys, data, lat, lon)

#     # Simulate passing time beyond cache duration
#     mock_datetime_now.return_value += timedelta(
#         minutes=weather_cache.cache_duration_minutes + 1
#     )

#     # Act
#     retrieved_data = weather_cache.get(cache_keys, lat, lon)

#     # Assert
#     assert retrieved_data is None


def test_set_removes_old_entry_for_same_request(weather_cache):
    """Test that setting a new entry for the same request removes the old one."""
    # Arrange
    cache_keys = ["temperature"]
    lat, lon = 51.5074, -0.1278
    old_data = {"value": 25.0}
    new_data = {"value": 26.0}

    # Act
    weather_cache.set(cache_keys, old_data, lat, lon)
    assert len(weather_cache.store) == 1
    weather_cache.set(cache_keys, new_data, lat, lon)

    # Assert
    assert len(weather_cache.store) == 1
    retrieved_data = weather_cache.get(cache_keys, lat, lon)
    assert retrieved_data == new_data


# def test_set_removes_expired_entries(weather_cache, mock_datetime_now):
#     """Test that expired entries are removed when a new entry is set."""
#     # Arrange
#     expired_keys = ["old_data"]
#     expired_data = {"value": 10.0}
#     lat, lon = 51.5074, -0.1278

#     weather_cache.set(expired_keys, expired_data, lat, lon)
#     assert len(weather_cache.store) == 1

#     # Simulate passing time to make the entry expired
#     mock_datetime_now.return_value += timedelta(
#         minutes=weather_cache.cache_duration_minutes + 1
#     )

#     # Act: set a new, non-matching entry
#     new_keys = ["new_data"]
#     new_data = {"value": 20.0}
#     weather_cache.set(new_keys, new_data, lat, lon)

#     # Assert
#     assert len(weather_cache.store) == 1
#     assert weather_cache.get(expired_keys, lat, lon) is None
#     assert weather_cache.get(new_keys, lat, lon) == new_data


def test_clear_method(weather_cache):
    """Test that the clear() method empties the cache."""
    # Arrange
    weather_cache.set(["key1"], {"data": 1}, 51.5, -0.1)
    weather_cache.set(["key2"], {"data": 2}, 51.6, -0.2)
    assert len(weather_cache.store) == 2

    # Act
    weather_cache.clear()

    # Assert
    assert len(weather_cache.store) == 0


# def test_get_stats(weather_cache, mock_datetime_now):
#     """Test that get_stats() returns the correct statistics."""
#     # Arrange: Add an active entry and an expired entry
#     weather_cache.set(["active"], {"data": 1}, 51.5, -0.1)

#     mock_datetime_now.return_value += timedelta(
#         minutes=weather_cache.cache_duration_minutes + 1
#     )
#     weather_cache.set(["expired"], {"data": 2}, 51.6, -0.2)

#     # Act
#     stats = weather_cache.get_stats()

#     # Assert
#     assert stats["total_entries"] == 2
#     assert stats["expired_entries"] == 1
#     assert stats["active_entries"] == 1
#     assert stats["cache_duration_minutes"] == 30


class TestWeatherCacheEntry:
    """Test cases for the WeatherCacheEntry dataclass"""

    def test_is_expired_true(self):
        """Test cache entry expiration - expired case"""
        old_timestamp = datetime.now() - timedelta(minutes=45)
        entry = WeatherCacheEntry(
            data="test_data",
            timestamp=old_timestamp,
            latitude=51.5074,
            longitude=-0.1278,
            cache_keys=["CURRENT"],
        )

        assert entry.is_expired(cache_duration_minutes=30) is True

    def test_is_expired_false(self):
        """Test cache entry expiration - not expired case"""
        recent_timestamp = datetime.now() - timedelta(minutes=15)
        entry = WeatherCacheEntry(
            data="test_data",
            timestamp=recent_timestamp,
            latitude=51.5074,
            longitude=-0.1278,
            cache_keys=["CURRENT"],
        )

        assert entry.is_expired(cache_duration_minutes=30) is False

    def test_matches_request_exact_match(self):
        """Test request matching with exact coordinates"""
        entry = WeatherCacheEntry(
            data="test_data",
            timestamp=datetime.now(),
            latitude=51.5074,
            longitude=-0.1278,
            cache_keys=["CURRENT"],
        )

        assert entry.matches_request(["CURRENT"], 51.5074, -0.1278) is True

    def test_matches_request_within_tolerance(self):
        """Test request matching within coordinate tolerance and key order"""
        entry = WeatherCacheEntry(
            data="test_data",
            timestamp=datetime.now(),
            latitude=51.5074,
            longitude=-0.1278,
            cache_keys=["CURRENT", "DAILY"],
        )

        # Slightly different coordinates (within ~100m)
        # Different order of keys
        assert entry.matches_request(["DAILY", "CURRENT"], 51.5075, -0.1279) is True

    def test_matches_request_different_type(self):
        """Test request matching with different data type"""
        entry = WeatherCacheEntry(
            data="test_data",
            timestamp=datetime.now(),
            latitude=51.5074,
            longitude=-0.1278,
            cache_keys=["CURRENT"],
        )

        assert entry.matches_request(["DAILY"], 51.5074, -0.1278) is False
