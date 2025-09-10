"""Integration tests for WeatherService"""

import pytest
from unittest.mock import patch, Mock
from datetime import datetime
from app.schemas.WeatherData import WeatherForecastData, WeatherDailyForecastData

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
            result = await self.weather_service.get_current_weather(**sample_coordinates)

            # Second call should use cache
            refetch_result = await self.weather_service.get_current_weather(**sample_coordinates)

            # Verify API was only called once
            mock_fetch.assert_called_once()

            # Both results should be the same
            assert result is refetch_result
            assert isinstance(result, WeatherForecastData)

            # Mapped values should be as expected
            assert result.weather_code == 2
            assert result.is_day == 1
            assert "2024-09-09T09:00" in result.time.isoformat()

            assert result.temperature.value == 16.2
            assert result.temperature.unit == "°C"

    @pytest.mark.asyncio
    async def test_get_daily_weather_full_flow(self, sample_coordinates, mock_daily_weather_api_response):
        """Test complete current weather flow with caching"""
        with patch.object(self.weather_service.api_client, 'fetch_weather_data') as mock_fetch:
            # Setup mocks
            mock_fetch.return_value = mock_daily_weather_api_response

            # First call should hit API
            result = await self.weather_service.get_daily_weather(**sample_coordinates)

            # Second call should use cache
            refetch_result = await self.weather_service.get_daily_weather(**sample_coordinates)

            # Verify API was only called once
            mock_fetch.assert_called_once()

            # Both results should be the same
            assert result is refetch_result
            assert isinstance(result, list)
            assert len(result) == 3
            today_result = result[0]
            assert isinstance(today_result, WeatherDailyForecastData)

            # Mapped values should be as expected

            assert today_result.weather_code == 80
            assert "2024-09-09" in today_result.time.isoformat()
            assert "2024-09-09T05:26" in today_result.sunrise.isoformat()

            assert today_result.temperature.max == 20.0
            assert today_result.temperature.min == 12.5
            assert today_result.temperature.unit == "°C"

    @pytest.mark.asyncio
    async def test_cache_expiration(self, sample_coordinates, mock_current_weather_api_response):
        """Test that expired cache entries are not used"""
        # Set short cache duration
        weather_service_short_cache = WeatherService(
            cache_duration_minutes=0.01)

        with patch.object(weather_service_short_cache.api_client, 'fetch_weather_data') as mock_fetch:
            mock_fetch.return_value = mock_current_weather_api_response

            # First call
            await weather_service_short_cache.get_current_weather(**sample_coordinates)

            # Wait for cache to expire
            import asyncio
            await asyncio.sleep(0.7)

            # Second call should hit API again
            await weather_service_short_cache.get_current_weather(**sample_coordinates)

            # API should have been called twice
            assert mock_fetch.call_count == 2

    def test_cache_stats(self):
        """Test cache statistics functionality"""
        # Add some mock cache entries
        now = datetime.now()
        expired_entry = Mock()
        expired_entry.is_expired.return_value = True
        active_entry = Mock()
        active_entry.is_expired.return_value = False

        self.weather_service.cache.store = [
            expired_entry, active_entry, active_entry]

        stats = self.weather_service.get_cache_stats()

        assert stats["total_entries"] == 3
        assert stats["expired_entries"] == 1
        assert stats["active_entries"] == 2
        assert stats["cache_duration_minutes"] == 30

    def test_clear_cache(self):
        """Test cache clearing"""
        # Add mock entries
        active_entry = Mock()
        active_entry.is_expired.return_value = False
        self.weather_service.cache.store = [
            active_entry, active_entry]
        assert len(self.weather_service.cache.store) == 2

        self.weather_service.clear_cache()
        assert len(self.weather_service.cache.store) == 0
