"""Unit tests for WeatherAPIClient"""

import asyncio
from unittest.mock import AsyncMock, Mock, patch

import pytest
import httpx

from app.services.weather.api_client import WeatherAPIClient
from app.services.weather.exceptions import (
    WeatherAPITimeoutError,
    WeatherAPIHTTPError,
    WeatherServiceError,
)
from app.services.weather.models import WeatherApiParams


@pytest.fixture(name="api_client")
def fixture_api_client() -> WeatherAPIClient:
    """Mock api client fixture"""
    return WeatherAPIClient(
        "https://api.test.com", timeout=30.0, cache_duration_minutes=0.01
    )


class TestWeatherAPIClient:
    """Test cases for the WeatherAPIClient"""

    @pytest.mark.asyncio
    async def test_fetch_weather_data_success(
        self, api_client, sample_coordinates, mock_current_weather_api_response
    ):
        """Test successful API data fetch"""
        with patch("httpx.AsyncClient") as mock_client:
            # Setup mock response
            mock_response = AsyncMock()
            mock_response.json = Mock(return_value=mock_current_weather_api_response)
            mock_response.raise_for_status = Mock()

            mock_client.return_value.__aenter__.return_value.get.return_value = (
                mock_response
            )

            params: WeatherApiParams = {
                **sample_coordinates,
                "current": ["temperature"],
            }
            result = await api_client.fetch_weather_data(params)

            mock_client.return_value.__aenter__.return_value.get.assert_called_once_with(
                "https://api.test.com/forecast", params=params
            )
            assert result["current"]["weather_code"] == 2
            assert result["current"]["time"] == "2024-09-09T09:00"

    @pytest.mark.asyncio
    async def test_fetch_weather_data_success_with_caching(
        self, api_client, sample_coordinates, mock_current_weather_api_response
    ):
        """Test successful API data fetch with caching"""
        with patch("httpx.AsyncClient") as mock_client:
            # Setup mock response
            mock_response = AsyncMock()
            mock_response.json = Mock(return_value=mock_current_weather_api_response)
            mock_response.raise_for_status = Mock()

            mock_client.return_value.__aenter__.return_value.get.return_value = (
                mock_response
            )

            params: WeatherApiParams = {
                **sample_coordinates,
                "daily": ["temperature"],
                "forecast_days": 3,
            }
            result = await api_client.fetch_weather_data(params)

            mock_client.return_value.__aenter__.return_value.get.assert_called_once_with(
                "https://api.test.com/forecast", params=params
            )

            assert result["current"]["time"] == "2024-09-09T09:00"

            # Make same request again within timeout
            await api_client.fetch_weather_data(params)

            assert mock_client.return_value.__aenter__.return_value.get.call_count == 1

            # Wait for cache to expire
            await asyncio.sleep(1)

            # Second call should hit API again
            await api_client.fetch_weather_data(params)

            # API should have been called twice
            assert mock_client.return_value.__aenter__.return_value.get.call_count == 2

    @pytest.mark.asyncio
    async def test_fetch_weather_data_timeout(self, api_client):
        """Test API timeout handling"""
        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.get.side_effect = (
                httpx.TimeoutException("Timeout")
            )

            with pytest.raises(WeatherAPITimeoutError) as exc_info:
                await api_client.fetch_weather_data({"test": "param"})

            assert "Weather service timeout" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_fetch_weather_data_http_error(self, api_client):
        """Test HTTP error handling"""
        with patch("httpx.AsyncClient") as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 404
            mock_response.raise_for_status = Mock(
                side_effect=httpx.HTTPStatusError(
                    "Not found",
                    request=httpx.Request("GET", "http://test.com"),
                    response=mock_response,
                )
            )

            mock_client.return_value.__aenter__.return_value.get.return_value = (
                mock_response
            )

            with pytest.raises(WeatherAPIHTTPError) as exc_info:
                await api_client.fetch_weather_data({"test": "param"})

            assert "Weather API error: 404" in str(exc_info.value)
            assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_fetch_weather_data_unexpected_error(self, api_client):
        """Test unexpected error handling"""
        with patch("httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.get.side_effect = (
                Exception("Unexpected error")
            )

            with pytest.raises(WeatherServiceError) as exc_info:
                await api_client.fetch_weather_data({"test": "param"})

            assert "Weather service unavailable" in str(exc_info.value)

    # @pytest.mark.asyncio
    # async def test_cache_expiration(
    #     self, sample_coordinates, mock_current_weather_api_response
    # ):
    #     """Test that expired cache entries are not used"""
    #     # Set short cache duration
    #     weather_service_short_cache = WeatherService(cache_duration_minutes=0.01)

    #     with patch.object(
    #         weather_service_short_cache.api_client, "fetch_weather_data"
    #     ) as mock_fetch:
    #         mock_fetch.return_value = mock_current_weather_api_response

    #         # First call
    #         await weather_service_short_cache.get_current_weather(**sample_coordinates)

    #         # Wait for cache to expire
    #         import asyncio

    #         await asyncio.sleep(0.7)

    #         # Second call should hit API again
    #         await weather_service_short_cache.get_current_weather(**sample_coordinates)

    #         # API should have been called twice
    #         assert mock_fetch.call_count == 2

    # def test_cache_stats(self):
    #     """Test cache statistics functionality"""
    #     # Add some mock cache entries
    #     now = datetime.now()
    #     expired_entry = Mock()
    #     expired_entry.is_expired.return_value = True
    #     active_entry = Mock()
    #     active_entry.is_expired.return_value = False

    #     self.weather_service.cache.store = [expired_entry, active_entry, active_entry]

    #     stats = self.weather_service.get_cache_stats()

    #     assert stats["total_entries"] == 3
    #     assert stats["expired_entries"] == 1
    #     assert stats["active_entries"] == 2
    #     assert stats["cache_duration_minutes"] == 30

    # def test_clear_cache(self):
    #     """Test cache clearing"""
    #     # Add mock entries
    #     active_entry = Mock()
    #     active_entry.is_expired.return_value = False
    #     self.weather_service.cache.store = [active_entry, active_entry]
    #     assert len(self.weather_service.cache.store) == 2

    #     self.weather_service.clear_cache()
    #     assert len(self.weather_service.cache.store) == 0
