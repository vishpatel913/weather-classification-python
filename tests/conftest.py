"""Pytest configuration and fixtures for tests"""

from httpx import Response
import pytest
import respx
from app.config import settings
from .mocks.weather_data_mocks import (
    mock_coordinates,
    mock_base_api_response_data,
    mock_current_weather_api_response_data,
    mock_daily_weather_api_response_data,
    mock_hourly_weather_api_response_data,
)


# MOCK API
@pytest.fixture(name="weather_api_mock")
def fixtures_weather_api_mock():
    """Fixture to mock weather API calls"""
    with respx.mock(
        base_url=settings.weather_api_base_url, assert_all_called=True
    ) as respx_mock:
        forecast_route = respx_mock.get("/forecast", name="forecast")
        forecast_route.return_value = Response(200, json=[])
        yield respx_mock


# MOCK DATA
@pytest.fixture
def sample_coordinates():
    """Fixture for test coordinates"""
    return mock_coordinates


@pytest.fixture
def mock_current_weather_api_response():
    """Mock response for weather API requesting current forecast"""
    return {**mock_base_api_response_data, **mock_current_weather_api_response_data}


@pytest.fixture
def mock_daily_weather_api_response():
    """Mock response for weather API requesting daily forecast (3 days)"""
    return {**mock_base_api_response_data, **mock_daily_weather_api_response_data}


@pytest.fixture
def mock_hourly_weather_api_response():
    """Mock response for weather API requesting hourly forecast (5 hours)"""
    return {**mock_base_api_response_data, **mock_hourly_weather_api_response_data}
