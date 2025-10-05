# """Integration tests for current weather endpoint"""

import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture(name="test_client")
def fixture_test_client():
    """Fixture for test coordinates"""
    return TestClient(app)


class TestHourlyWeatherEndpoint:
    """Test cases for the hourly weather endpoint"""

    @pytest.mark.asyncio
    async def test_weather_hourly_successful(
        self,
        *,
        test_client,
        weather_api_mock,
        sample_coordinates,
        mock_hourly_weather_api_response,
        mock_daily_weather_api_response,
    ):
        """Test hourly weather when services are healthy"""
        weather_api_mock["forecast"].respond(
            json={
                **mock_hourly_weather_api_response,
                **mock_daily_weather_api_response,
            },
            status_code=200,
        )

        result = test_client.get(
            (
                "/prod/api/v1/weather/hourly?"
                "forecast_length=1&"
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
            "hourly",
        ]
        assert all(key in data for key in expected_response_fields)

        assert data["latitude"] == sample_coordinates["latitude"]
        assert data["longitude"] == sample_coordinates["longitude"]
        assert data["forecast_length"] == 1

        hourly_result = data["hourly"]
        # number of results in mock
        assert len(hourly_result) == 5

        first_hour_result = hourly_result[0]
        expected_hourly_fields = [
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
        assert all(key in first_hour_result for key in expected_hourly_fields)

        assert "2024-09-09T09:00" in first_hour_result["time"]
        assert first_hour_result["weather_code"] == 1
        assert first_hour_result["is_day"] == 1
        assert first_hour_result["temperature"]["value"] == 15.9
        assert first_hour_result["temperature"]["unit"] == "°C"
