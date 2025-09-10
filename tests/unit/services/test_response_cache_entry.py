# TODO: make reusable and move to models
"""Unit tests for ResponseCacheEntry"""

import pytest
from datetime import datetime, timedelta

from app.services.weather.models import ResponseCacheEntry


class TestResponseCacheEntry:
    """Test cases for the ResponseCacheEntry class"""

    def test_is_expired_true(self):
        """Test cache entry expiration - expired case"""
        old_timestamp = datetime.now() - timedelta(minutes=45)
        entry = ResponseCacheEntry(
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
        entry = ResponseCacheEntry(
            data="test_data",
            timestamp=recent_timestamp,
            latitude=51.5074,
            longitude=-0.1278,
            cache_keys=["CURRENT"],
        )

        assert entry.is_expired(cache_duration_minutes=30) is False

    def test_matches_request_exact_match(self):
        """Test request matching with exact coordinates"""
        entry = ResponseCacheEntry(
            data="test_data",
            timestamp=datetime.now(),
            latitude=51.5074,
            longitude=-0.1278,
            cache_keys=["CURRENT"],
        )

        assert entry.matches_request(["CURRENT"], 51.5074, -0.1278) is True

    def test_matches_request_within_tolerance(self):
        """Test request matching within coordinate tolerance and key order"""
        entry = ResponseCacheEntry(
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
        entry = ResponseCacheEntry(
            data="test_data",
            timestamp=datetime.now(),
            latitude=51.5074,
            longitude=-0.1278,
            cache_keys=["CURRENT"],
        )

        assert entry.matches_request(["DAILY"], 51.5074, -0.1278) is False
