"""Integration tests for WeatherService"""

import pytest
from unittest.mock import patch, AsyncMock, Mock
from datetime import datetime, timedelta
from app.schemas.WeatherData import WeatherForecastData

from app.services.weather.service import WeatherService


class TestWeatherServiceIntegration:
    """Integration test cases for the complete WeatherService"""

    def setup_method(self):
        """Set up weather service instance"""
        self.weather_service = WeatherService()

    @pytest.mark.asyncio
    async def test_get_current_weather_full_flow(self, sample_coordinates, mock_current_weather_api_response):
        """Test complete current weather flow with caching"""
        with patch.object(self.weather_service.api_client, 'fetch_weather_data') as mock_fetch:
            # Setup mocks
            mock_fetch.return_value = mock_current_weather_api_response

            # First call should hit API
            result1 = await self.weather_service.get_current_weather(**sample_coordinates)

            # Second call should use cache
            result2 = await self.weather_service.get_current_weather(**sample_coordinates)

            # Verify API was only called once
            mock_fetch.assert_called_once()

            # Both results should be the same
            assert result1 is result2
            assert isinstance(result1, WeatherForecastData)

    @pytest.mark.asyncio
    async def test_cache_expiration(self, sample_coordinates):
        """Test that expired cache entries are not used"""
        # Set very short cache duration
        self.weather_service.cache_duration_minutes = 0.01  # ~0.6 seconds

        with patch.object(self.weather_service.api_client, 'fetch_weather_data') as mock_fetch:
            mock_fetch.return_value = {"current": {}}

            # First call
            await self.weather_service.get_current_weather(**sample_coordinates)

            # Wait for cache to expire
            import asyncio
            await asyncio.sleep(0.7)

            # Second call should hit API again
            await self.weather_service.get_current_weather(**sample_coordinates)

            # API should have been called twice
            assert mock_fetch.call_count == 2

    def test_cache_stats(self, weather_service):
        """Test cache statistics functionality"""
        # Add some mock cache entries
        now = datetime.now()
        expired_entry = Mock()
        expired_entry.is_expired.return_value = True
        active_entry = Mock()
        active_entry.is_expired.return_value = False

        weather_service.cache = [expired_entry, active_entry, active_entry]

        stats = weather_service.get_cache_stats()

        assert stats["total_entries"] == 3
        assert stats["expired_entries"] == 1
        assert stats["active_entries"] == 2
        assert stats["cache_duration_minutes"] == 30

    def test_clear_cache(self, weather_service):
        """Test cache clearing"""
        # Add mock entries
        weather_service.cache = [Mock(), Mock()]
        assert len(weather_service.cache) == 2

        weather_service.clear_cache()
        assert len(weather_service.cache) == 0
