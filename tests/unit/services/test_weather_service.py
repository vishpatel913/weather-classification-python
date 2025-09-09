import pytest
from unittest.mock import AsyncMock, patch
import httpx
from datetime import datetime

from app.services.WeatherService import WeatherService, WeatherServiceError
from app.schemas.WeatherData import WeatherForecastData

from ..weather_data_mocks import mock_current_weather_api_response


class TestWeatherService:
    """Test cases for the WeatherService"""

    def setup_method(self):
        """Set up weather service instance"""
        self.weather_service = WeatherService()

    @pytest.mark.asyncio
    async def test_get_current_weather_success(self):
        """Test successful weather data retrieval"""
        with patch('httpx.AsyncClient') as mock_client:
            # Mock successful API response
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_response.json.return_value = mock_current_weather_api_response

            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response

            current_result = await self.weather_service.get_current_weather(51.5074, -0.1278)

            # expected_fields = ["temperature", "wind_speed"]
            # assert all(key in current_result for key in expected_fields)
            assert isinstance(current_result, WeatherForecastData)

            assert current_result.weather_code == 2
            assert current_result.is_day == 1
            assert "2024-09-09T09:00" in current_result.time.isoformat()

            assert current_result.temperature.value == 16.2
            assert current_result.temperature.unit == "°C"
            assert current_result.wind_speed.value == 6.5
            assert current_result.wind_speed.unit == "km/h"
            assert current_result.precipitation.value == 0.12
            assert current_result.precipitation.unit == "mm"
            assert current_result.cloud_cover.value == 15
            assert current_result.cloud_cover.unit == "%"
            assert current_result.uv_index.value == 2.85
            assert current_result.uv_index.unit == ""

    @pytest.mark.asyncio
    async def test_get_current_weather_http_error(self):
        """Test weather data retrieval with HTTP error"""
        with patch('httpx.AsyncClient') as mock_client:
            # Mock HTTP error
            mock_response = AsyncMock()
            mock_response.status_code = 404
            mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
                "Not found", request=AsyncMock(), response=mock_response
            )

            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response

            with pytest.raises(WeatherServiceError) as exc_info:
                await self.weather_service.get_current_weather(51.5074, -0.1278)

            assert "Weather API error" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_current_weather_timeout(self):
        """Test weather data retrieval with timeout"""
        with patch('httpx.AsyncClient') as mock_client:
            # Mock timeout
            mock_client.return_value.__aenter__.return_value.get.side_effect = httpx.TimeoutException(
                "Timeout")

            with pytest.raises(WeatherServiceError) as exc_info:
                await self.weather_service.get_current_weather(51.5074, -0.1278)

            assert "Weather service timeout" in str(exc_info.value)

    @pytest.mark.asyncio
    async def test_get_current_weather_invalid_data(self):
        """Test weather data retrieval with invalid response format"""
        with patch('httpx.AsyncClient') as mock_client:
            # Mock response with missing data
            mock_response = AsyncMock()
            mock_response.status_code = 200
            mock_response.json.return_value = {
                "current": {
                    # "temperature_2m": 22.5
                    # Missing other required fields
                }
            }

            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response

            with pytest.raises(WeatherServiceError) as exc_info:
                await self.weather_service.get_current_weather(51.5074, -0.1278)

            assert "Invalid weather data format" in str(exc_info.value)
