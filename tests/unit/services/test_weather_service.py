import pytest
from unittest.mock import AsyncMock, patch
import httpx
from datetime import datetime

from app.services.WeatherService import WeatherService, WeatherServiceError
from app.schemas.Weather import WeatherConditions
# from app.schemas.WeatherData import WeatherForecastData


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
                    "apparent_temperature": "°C",
                    "relative_humidity_2m": "%",
                    "wind_speed_10m": "km/h",
                    "precipitation": "mm",
                    "precipitation_probability": "%",
                    "cloud_cover": "%",
                    "uv_index": "",
                },
                "current": {
                    "time": "2023-09-09T09:00",
                    "interval": 900,
                    "weather_code": 1,
                    "is_day": 1,
                    "temperature_2m": 16.2,
                    "apparent_temperature": 15.6,
                    "relative_humidity_2m": 71,
                    "wind_speed_10m": 6.5,
                    "precipitation": 0.00,
                    "precipitation_probability": 0,
                    "cloud_cover": 15,
                    "uv_index": 2.85,
                },
            }

            mock_client.return_value.__aenter__.return_value.get.return_value = mock_response

            current_result = await self.weather_service.get_current_weather(51.5074, -0.1278)

            assert isinstance(current_result, WeatherConditions)
            assert current_result.temperature == 16.2
            assert current_result.humidity == 71
            assert current_result.wind_speed == 6.5
            assert current_result.precipitation == 0.00
            assert current_result.cloud_cover == 15
            assert current_result.uv_index == 2.85

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
