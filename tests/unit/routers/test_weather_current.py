import pytest

# from unittest.mock import patch
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(name="client")
def fixture_test_client():
    """Fixture for test coordinates"""
    return TestClient(app)


class TestCurrentWeatherEndpoint:
    """Test cases for the current weather endpoint"""

    # @patch('app.routers.base_router.health_check')
    def test_weather_current_successful(self, client):
        """Test weather when services are unhealthy"""

        response = client.get("/prod/api/v1/weather/current")

        assert response
