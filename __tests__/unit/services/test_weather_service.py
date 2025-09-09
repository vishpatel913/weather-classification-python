import pytest
from unittest.mock import AsyncMock, patch
import httpx
from datetime import datetime

from app.services.WeatherService import WeatherService, WeatherServiceError
from app.schemas.Weather import WeatherConditions


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
            mock_response.json.return_value = {
                "latitude": 51.5,
                "longitude": -0.120000124,
                "generationtime_ms": 0.108957290649414,
                "utc_offset_seconds": 3600,
                "timezone": "Europe/London",
                "timezone_abbreviation": "GMT+1",
                "elevation": 23,
                "current_units": {
                    "time": "iso8601",
                    "interval": "seconds",
                    "weather_code": "wmo code",
                    "is_day": "",
                    "temperature_2m": "°C",
                    "relative_humidity_2m": "%",
                    "apparent_temperature": "°C",
                    "wind_speed_10m": "km/h",
                    "precipitation": "mm",
                    "precipitation_probability": "%",
                    "cloud_cover": "%",
                    "uv_index": ""
                },
                "current": {
                    "time": "2025-09-06T09:30",
                    "interval": 900,
                    "weather_code": 3,
                    "is_day": 1,
                    "temperature_2m": 22.5,
                    "relative_humidity_2m": 65.0,
                    "apparent_temperature": 16.3,
                    "wind_speed_10m": 10.0,
                    "precipitation": 0.0,
                    "precipitation_probability": 0,
                    "cloud_cover": 40.0,
                    "uv_index": 5.0
                }
            }

            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response

            weather = await self.weather_service.get_current_weather(51.5074, -0.1278)

            assert isinstance(weather, WeatherConditions)
            assert weather.temperature == 22.5
            assert weather.humidity == 65.0
            assert weather.wind_speed == 10.0
            assert weather.precipitation == 0.0
            assert weather.cloud_cover == 40.0
            assert weather.uv_index == 5.0

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
