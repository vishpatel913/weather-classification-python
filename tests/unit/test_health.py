import pytest
from unittest.mock import patch, AsyncMock
from fastapi.testclient import TestClient

from app.main import app
from app.models.schemas import HealthStatus


class TestHealthEndpoint:
    """Test cases for the health check endpoint"""

    def setup_method(self):
        """Set up test client"""
        self.client = TestClient(app)

    @patch('app.api.dependencies.get_health_check')
    def test_health_check_healthy(self, mock_get_health):
        """Test health check when all services are healthy"""
        # Mock a healthy response
        from app.models.schemas import HealthCheck, ServiceCheck
        from datetime import datetime

        mock_health = HealthCheck(
            status=HealthStatus.HEALTHY,
            timestamp=datetime.now(),
            version="0.1.0",
            uptime_seconds=123.45,
            checks=[
                ServiceCheck(
                    name="weather_api",
                    status=HealthStatus.HEALTHY,
                    response_time_ms=150.0
                ),
                ServiceCheck(
                    name="clothing_recommender",
                    status=HealthStatus.HEALTHY,
                    response_time_ms=5.0
                )
            ]
        )

        mock_get_health.return_value = mock_health

        response = self.client.get("/api/v1/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "version" in data
        assert "uptime_seconds" in data
        assert "checks" in data
        assert len(data["checks"]) == 2

    @patch('app.api.dependencies.get_health_check')
    def test_health_check_unhealthy(self, mock_get_health):
        """Test health check when services are unhealthy"""
        from app.models.schemas import HealthCheck
        from datetime import datetime

        mock_health = HealthCheck(
            status=HealthStatus.UNHEALTHY,
            timestamp=datetime.now(),
            version="0.1.0",
            uptime_seconds=123.45,
            checks=[]
        )

        mock_get_health.return_value = mock_health

        response = self.client.get("/api/v1/health")

        # Should return 503 for unhealthy status
        assert response.status_code == 503

    @patch('app.api.dependencies.get_health_check')
    def test_health_check_degraded(self, mock_get_health):
        """Test health check when services are degraded"""
        from app.models.schemas import HealthCheck
        from datetime import datetime

        mock_health = HealthCheck(
            status=HealthStatus.DEGRADED,
            timestamp=datetime.now(),
            version="0.1.0",
            uptime_seconds=123.45,
            checks=[]
        )

        mock_get_health.return_value = mock_health

        response = self.client.get("/api/v1/health")

        # Should return 200 for degraded (service still working)
        assert response.status_code == 200
        assert response.json()["status"] == "degraded"

    def test_health_check_response_format(self):
        """Test that health check response has correct format"""
        response = self.client.get("/api/v1/health")

        # Should be 200 or 503, but always return JSON
        assert response.status_code in [200, 503]

        data = response.json()
        required_fields = ["status", "timestamp",
                           "version", "uptime_seconds", "checks"]

        for field in required_fields:
            assert field in data

        assert isinstance(data["checks"], list)
        assert isinstance(data["uptime_seconds"], (int, float))


@pytest.mark.integration
class TestHealthEndpointIntegration:
    """Integration tests for health endpoint with real dependencies"""

    @pytest.mark.slow
    def test_real_health_check(self):
        """Test health check with real dependencies (may be slow)"""
        with TestClient(app) as client:
            response = client.get("/api/v1/health")

            # Should return some response (may be degraded if external APIs are down)
            assert response.status_code in [200, 503]

            data = response.json()
            assert "status" in data
            assert "checks" in data

            # Should have both weather_api and clothing_recommender checks
            check_names = [check["name"] for check in data["checks"]]
            assert "weather_api" in check_names
            assert "clothing_recommender" in check_names
