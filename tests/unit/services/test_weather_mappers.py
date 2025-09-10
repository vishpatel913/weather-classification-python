import pytest
from unittest.mock import AsyncMock, Mock, patch
import httpx
from datetime import datetime

from app.schemas.WeatherData import WeatherForecastData, WeatherDailyForecastData
from app.services.weather.exceptions import WeatherAPIFormatError
from app.services.weather.mappers import map_current_weather, map_daily_weather


class TestWeatherMappers:
    """Test cases for the response mapper utils"""

    def test_map_current_weather_success(self, mock_current_weather_api_response):
        """Test successful current weather data retrieval"""
        result = map_current_weather(mock_current_weather_api_response)

        # expected_fields = ["temperature", "wind_speed"]
        # assert all(key in result for key in expected_fields)
        assert isinstance(result, WeatherForecastData)

        assert result.weather_code == 2
        assert result.is_day == 1
        assert "2024-09-09T09:00" in result.time.isoformat()

        assert result.temperature.value == 16.2
        assert result.temperature.unit == "°C"
        assert result.wind_speed.value == 6.5
        assert result.wind_speed.unit == "km/h"
        assert result.precipitation.value == 0.12
        assert result.precipitation.unit == "mm"
        assert result.cloud_cover.value == 15
        assert result.cloud_cover.unit == "%"
        assert result.uv_index.value == 2.85
        assert result.uv_index.unit == ""

    def test_map_current_weather_missing_current_key(self):
        """Test current weather mapping with missing 'current' key"""
        invalid_response = {"daily": {"temperature": 20}}

        with pytest.raises(WeatherAPIFormatError) as exc_info:
            map_current_weather(invalid_response)

        assert "Invalid current weather data format" in str(exc_info.value)

    def test_map_current_weather_missing_current_fields(self):
        """Test current weather mapping with missing 'current' fields"""
        invalid_response = {
            "current": {
                "temperature_2m": 22.5,
                "cloud_cover": "invalid",
                # Missing other required fields
            },
            "current_units": {},
        }

        with pytest.raises(WeatherAPIFormatError) as exc_info:
            map_current_weather(invalid_response)

            assert "Invalid current weather data format" in str(exc_info.value)

    def test_get_daily_weather_success(self, mock_daily_weather_api_response):
        """Test successful daily weather data retrieval"""
        result = map_daily_weather(mock_daily_weather_api_response)

        assert isinstance(result, list)
        assert len(result) == 3

        # testing today
        today_result = result[0]

        assert "2024-09-09" in today_result.time.isoformat()
        assert "2024-09-09T05:26" in today_result.sunrise.isoformat()
        assert today_result.temperature.max == 20.0
        assert today_result.temperature.min == 12.5
        assert today_result.temperature.unit == "°C"
        assert today_result.uv_index.max == 4.95
        assert today_result.precipitation_probability.max == 3.0
        assert today_result.precipitation_hours == 2.0

        # testing next day order
        assert "2024-09-10" in result[1].time.isoformat()
        assert "2024-09-11" in result[2].time.isoformat()

    def test_map_daily_weather_missing_daily_key(self):
        """Test daily weather mapping with missing 'daily' key"""
        invalid_response = {"daily": {"temperature": 20}}

        with pytest.raises(WeatherAPIFormatError) as exc_info:
            map_daily_weather(invalid_response)

        assert "Invalid daily weather data format" in str(exc_info.value)

    def test_map_daily_weather_missing_daily_fields(self):
        """Test daily weather mapping with missing 'daily' fields"""
        invalid_response = {
            "daily": {
                "temperature_2m_max": [22.5],
                "cloud_cover_min": ["invalid"],
                # Missing other required fields
            },
            "daily_units": {},
        }

        with pytest.raises(WeatherAPIFormatError) as exc_info:
            map_daily_weather(invalid_response)

        assert "Invalid daily weather data format" in str(exc_info.value)
