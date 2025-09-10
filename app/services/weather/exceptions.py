"""Weather service exception hierarchy"""


class WeatherServiceError(Exception):
    """Base exception for weather service errors"""
    pass


class WeatherAPITimeoutError(WeatherServiceError):
    """Raised when the weather API times out"""
    pass


class WeatherAPIHTTPError(WeatherServiceError):
    """Raised when the weather API returns an HTTP error"""
    def __init__(self, message: str, status_code: int):
        super().__init__(message)
        self.status_code = status_code


class WeatherAPIFormatError(WeatherServiceError):
    """Raised when the weather API returns unexpected data format"""
    pass
