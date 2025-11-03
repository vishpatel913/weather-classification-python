"""Integration tests for current weather endpoint"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(name="test_client")
def fixture_test_client():
    """Fixture for test coordinates"""
    return TestClient(app)


class TestDailyWeatherEndpoint:
    """Test cases for the daily weather endpoint"""

    @pytest.mark.asyncio
    async def test_weather_current_successful(
        self,
        *,
        test_client,
        weather_api_mock,
        sample_coordinates,
        mock_daily_weather_api_response,
    ):
        """Test daily weather when services are healthy"""
        weather_api_mock["forecast"].respond(
            json={
                **mock_daily_weather_api_response,
            },
            status_code=200,
        )

        result = test_client.get(
            (
                "/prod/api/v1/weather/daily?"
                "forecast_length=3&"
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
            "daily",
        ]
        assert all(key in data for key in expected_response_fields)

        assert data["latitude"] == sample_coordinates["latitude"]
        assert data["longitude"] == sample_coordinates["longitude"]
        assert data["forecast_length"] == 3

        daily_result = data["daily"]
        # number of results in mock
        assert len(daily_result) == 3

        expected_daily_fields = [
            "time",
            "weather_code",
            "sunrise",
            "sunset",
            "temperature",
            "precipitation_probability",
            "precipitation_hours",
            "uv_index",
        ]

        first_day_result = daily_result[0]
        assert all(key in first_day_result for key in expected_daily_fields)

        assert "2024-09-09" in first_day_result["time"]
        assert "2024-09-09T05:26" in first_day_result["sunrise"]
        assert "2024-09-09T18:29" in first_day_result["sunset"]

        assert first_day_result["weather_code"] == 80
        assert first_day_result["temperature"]["max"] == 20.0
        assert first_day_result["temperature"]["min"] == 12.5
        assert first_day_result["temperature"]["unit"] == "°C"

        third_day_result = daily_result[2]
        assert all(key in third_day_result for key in expected_daily_fields)

        assert "2024-09-11" in third_day_result["time"]
        assert "2024-09-11T05:29" in third_day_result["sunrise"]
        assert "2024-09-11T18:24" in third_day_result["sunset"]

        assert third_day_result["weather_code"] == 1
        assert third_day_result["temperature"]["max"] == 17.9
        assert third_day_result["temperature"]["min"] == 12.4
        assert third_day_result["temperature"]["unit"] == "°C"
