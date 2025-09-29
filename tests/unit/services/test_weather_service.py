"""Integration tests for WeatherService"""

from unittest.mock import patch
import pytest

from app.schemas.weather_data import WeatherForecastData, WeatherDailyForecastData
from app.services.weather.service import WeatherService


@pytest.fixture(name="weather_service")
def fixture_weather_service() -> WeatherService:
    """Mock api client fixture"""
    return WeatherService()


class TestWeatherServiceIntegration:
    """Integration test cases for the complete WeatherService"""

    @pytest.mark.asyncio
    async def test_get_current_weather_full_flow(
        self, weather_service, sample_coordinates, mock_current_weather_api_response
    ):
        """Test complete current weather flow"""
        with patch.object(
            weather_service.api_client, "fetch_weather_data"
        ) as mock_fetch:
            # Setup mocks
            mock_fetch.return_value = mock_current_weather_api_response

            result = await weather_service.get_current_weather(**sample_coordinates)

            # Verify API was only called once
            mock_fetch.assert_called_once()

            # Both results should be the same
            assert isinstance(result, WeatherForecastData)

            # Mapped values should be as expected
            assert result.weather_code == 2
            assert result.is_day == 1
            assert "2024-09-09T09:00" in result.time.isoformat()

            assert result.temperature.value == 16.2
            assert result.temperature.unit == "°C"

    @pytest.mark.asyncio
    async def test_get_daily_weather_full_flow(
        self, weather_service, sample_coordinates, mock_daily_weather_api_response
    ):
        """Test complete daily weather flow"""
        with patch.object(
            weather_service.api_client, "fetch_weather_data"
        ) as mock_fetch:
            # Setup mocks
            mock_fetch.return_value = mock_daily_weather_api_response

            result = await weather_service.get_daily_weather(**sample_coordinates)

            # Verify API was only called once
            mock_fetch.assert_called_once()

            # Both results should be the same
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
