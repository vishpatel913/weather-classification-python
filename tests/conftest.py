import pytest
from .mocks.weather_data_mocks import (
    mock_coordinates,
    mock_base_api_response_data,
    mock_current_weather_api_response_data,
    mock_daily_weather_api_response_data,
    mock_hourly_weather_api_response_data,
)


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
