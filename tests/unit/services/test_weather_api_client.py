"""Unit tests for WeatherAPIClient"""

import pytest
import httpx
from unittest.mock import AsyncMock, Mock, patch

from app.services.weather.api_client import WeatherAPIClient
from app.services.weather.exceptions import WeatherAPITimeoutError, WeatherAPIHTTPError, WeatherServiceError


class TestWeatherAPIClient:
    """Test cases for the WeatherAPIClient"""

    def setup_method(self):
        """Set up weather service instance"""
        self.api_client = WeatherAPIClient("https://api.test.com", 30.0)

    @pytest.mark.asyncio
    async def test_fetch_weather_data_success(self, mock_current_weather_api_response):
        """Test successful API data fetch"""
        with patch('httpx.AsyncClient') as mock_client:
            # Setup mock response
            mock_response = AsyncMock()
            mock_response.json = Mock(
                return_value=mock_current_weather_api_response)
            mock_response.raise_for_status = Mock()

            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response

            params = {"latitude": 51.5074, "longitude": -0.1278}
            result = await self.api_client.fetch_weather_data(params)

            mock_client.return_value.__aenter__.return_value.get.assert_called_once_with(
                "https://api.test.com/forecast", params=params
            )
            assert result["current"]["weather_code"] == 2
            assert result["current"]["time"] == "2024-09-09T09:00"

    @pytest.mark.asyncio
    async def test_fetch_weather_data_timeout(self):
        """Test API timeout handling"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.side_effect = httpx.TimeoutException(
                "Timeout")

            with pytest.raises(WeatherAPITimeoutError) as exc_info:
                await self.api_client.fetch_weather_data({"test": "param"})

            assert "Weather service timeout" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_fetch_weather_data_http_error(self):
        """Test HTTP error handling"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_response = AsyncMock()
            mock_response.status_code = 404
            mock_response.raise_for_status = Mock(side_effect=httpx.HTTPStatusError(
                "Not found",
                request=httpx.Request("GET", "http://test.com"),
                response=mock_response
            ))

            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response

            with pytest.raises(WeatherAPIHTTPError) as exc_info:
                await self.api_client.fetch_weather_data({"test": "param"})

            assert "Weather API error: 404" in str(exc_info.value)
            assert exc_info.value.status_code == 404

    @pytest.mark.asyncio
    async def test_fetch_weather_data_unexpected_error(self):
        """Test unexpected error handling"""
        with patch('httpx.AsyncClient') as mock_client:
            mock_client.return_value.__aenter__.return_value.get.side_effect = Exception(
                "Unexpected error")

            with pytest.raises(WeatherServiceError) as exc_info:
                await self.api_client.fetch_weather_data({"test": "param"})

            assert "Weather service unavailable" in str(exc_info.value)
