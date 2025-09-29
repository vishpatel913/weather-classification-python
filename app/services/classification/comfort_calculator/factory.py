"""Factory for ComfortCalculator"""

from app.models.weather_conditions import WeatherClassificationFields


class ComfortIndexCalculator:
    """Calculates comfort index based on values and their types"""

    def normalize(
        self, value: str | int | float, type: WeatherClassificationFields
    ) -> float:
        return 0.0
