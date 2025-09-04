import pytest
from unittest.mock import AsyncMock, patch
import httpx
from datetime import datetime

from app.services.weather_service import WeatherService, WeatherServiceError
from app.models.weather import WeatherConditions


class TestWeatherService:
    """Test cases for the WeatherService"""

    def setup_method(self):
        """Set up weather service instance"""
        self.weather_service = WeatherService()
