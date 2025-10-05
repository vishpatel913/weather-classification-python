"""Integration tests for current weather endpoint"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(name="test_client")
def fixture_test_client():
    """Fixture for test coordinates"""
    return TestClient(app)


class TestCurrentWeatherEndpoint:
    """Test cases for the current weather endpoint"""

    @pytest.mark.asyncio
    async def test_weather_current_successful(
        self,
        *,
        test_client,
        weather_api_mock,
        sample_coordinates,
        mock_current_weather_api_response,
        mock_daily_weather_api_response,
    ):
        """Test current weather when services are healthy"""
        weather_api_mock["forecast"].respond(
            json={
                **mock_current_weather_api_response,
                **mock_daily_weather_api_response,
            },
            status_code=200,
        )

        result = test_client.get(
            (
                "/prod/api/v1/weather/current?"
                f"latitude={sample_coordinates['latitude']}&"
                f"longitude={sample_coordinates['longitude']}"
            )
        )

        assert result.status_code == 200
        data = result.json()

        assert weather_api_mock["forecast"].calls.called
        assert weather_api_mock["forecast"].calls.call_count == 1

        expected_response_fields = [
            "timestamp",
            "latitude",
            "longitude",
            "forecast_length",
            "current",
            "today",
        ]
        assert all(key in data for key in expected_response_fields)

        assert data["latitude"] == sample_coordinates["latitude"]
        assert data["longitude"] == sample_coordinates["longitude"]

        current_result = data["current"]
        expected_current_fields = [
            "time",
            "weather_code",
            "is_day",
            "temperature",
            "apparent_temperature",
            "humidity",
            "wind_speed",
            "precipitation",
            "precipitation_probability",
            "cloud_cover",
            "uv_index",
        ]
        assert all(key in current_result for key in expected_current_fields)

        assert "2024-09-09T09:00" in current_result["time"]
        assert current_result["weather_code"] == 2
        assert current_result["is_day"] == 1
        assert current_result["temperature"]["value"] == 16.2
        assert current_result["temperature"]["unit"] == "°C"

        today_result = data["today"]
        expected_daily_fields = [
            "time",
            "weather_code",
            "sunrise",
            "sunset",
            "sunshine_duration",
            "temperature",
            "apparent_temperature",
            "precipitation_probability",
            "precipitation_hours",
            "uv_index",
        ]
        assert all(key in today_result for key in expected_daily_fields)

        assert "2024-09-09" in today_result["time"]
        assert "5:26:00" in today_result["sunrise"]
        assert today_result["weather_code"] == 80
        assert today_result["temperature"]["min"] == 12.5
        assert today_result["temperature"]["max"] == 20.0
        assert today_result["temperature"]["unit"] == "°C"
