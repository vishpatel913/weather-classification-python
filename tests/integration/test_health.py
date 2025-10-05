from fastapi.testclient import TestClient
import pytest


from app.main import app


@pytest.fixture(name="client")
def fixture_test_api_client() -> TestClient:
    """Mock api client fixture"""
    return TestClient(app)


class TestHealthEndpoint:
    """Test cases for the health check endpoint"""

    def test_health_check_response_format(self, client):
        """Test that health check response has correct format"""
        response = client.get("/prod/api/health")

        # Should be 200 or 503, but always return JSON
        assert response.status_code in [200, 503]

        data = response.json()
        required_fields = ["status", "timestamp", "version", "uptime_seconds"]

        for field in required_fields:
            assert field in data

        assert isinstance(data["uptime_seconds"], (int, float))


class TestHealthEndpointIntegration:
    """Integration tests for health endpoint with real dependencies"""

    def test_real_health_check(self):
        """Test health check with real dependencies (may be slow)"""
        with TestClient(app) as client:
            response = client.get("/prod/api/health")

            # Should return some response (may be degraded if external APIs are down)
            assert response.status_code in [200, 503]

            data = response.json()
            assert "status" in data
