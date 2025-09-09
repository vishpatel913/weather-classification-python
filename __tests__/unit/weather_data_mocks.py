mock_coordinates = {
    "latitude": 51.5,
    "longitude": -0.120000124,
}

mock_base_api_response = {
    **mock_coordinates,
    "generationtime_ms": 0.108957290649414,
    "utc_offset_seconds": 3600,
    "timezone": "Europe/London",
    "timezone_abbreviation": "GMT+1",
    "elevation": 23,
}

mock_current_weather_api_response = {
    **mock_base_api_response,
    "current_units": {
        "time": "iso8601",
        "interval": "seconds",
        "weather_code": "wmo code",
        "is_day": "",
        "temperature_2m": "°C",
        "apparent_temperature": "°C",
        "relative_humidity_2m": "%",
        "wind_speed_10m": "km/h",
        "precipitation": "mm",
        "precipitation_probability": "%",
        "cloud_cover": "%",
        "uv_index": "",
    },
    "current": {
        "time": "2023-09-09T09:00",
        "interval": 900,
        "weather_code": 1,
        "is_day": 1,
        "temperature_2m": 16.2,
        "apparent_temperature": 15.6,
        "relative_humidity_2m": 71,
        "wind_speed_10m": 6.5,
        "precipitation": 0.00,
        "precipitation_probability": 0,
        "cloud_cover": 15,
        "uv_index": 2.85,
    },
}

mock_daily_weather_api_response = {
    **mock_base_api_response,
    "daily_units": {
        "time": "iso8601",
        "weather_code": "wmo code",
        "sunrise": "iso8601",
        "sunset": "iso8601",
        "temperature_2m_max": "°C",
        "temperature_2m_min": "°C",
        "apparent_temperature_max": "°C",
        "apparent_temperature_min": "°C",
        "sunshine_duration": "s",
        "uv_index_max": "",
        "precipitation_probability_max": "%",
        "precipitation_hours": "h"
    },
    "daily": {
        "time": ["2023-09-09", "2025-09-10", "2025-09-11"],
        "weather_code": [80, 95, 80],
        "sunrise": ["2023-09-09T05:26", "2025-09-10T05:28", "2025-09-11T05:29"],
        "sunset": ["2023-09-09T18:29", "2025-09-10T18:26", "2025-09-11T18:24"],
        "temperature_2m_max": [20.0, 18.3, 17.9],
        "temperature_2m_min": [12.5, 15.0, 12.4],
        "apparent_temperature_max": [18.1, 16.7, 14.4],
        "apparent_temperature_min": [12.6, 13.3, 9.8],
        "sunshine_duration": [39721.41, 8371.14, 39501.82],
        "uv_index_max": [4.95, 4.10, 4.85],
        "precipitation_probability_max": [3, 68, 73],
        "precipitation_hours": [2.0, 10.0, 7.0]
    }
}

mock_hourly_weather_api_response = {
    **mock_base_api_response,
    "hourly_units": {
        "time": "iso8601",
        "weather_code": "wmo code",
        "is_day": "",
        "temperature_2m": "°C",
        "apparent_temperature": "°C",
        "relative_humidity_2m": "%",
        "wind_speed_10m": "km/h",
        "precipitation": "mm",
        "precipitation_probability": "%",
        "cloud_cover": "%",
        "uv_index": "",
        "visibility": "m"
    },
    "hourly": {
        "time": ["2025-09-09T09:00", "2025-09-09T10:00", "2025-09-09T11:00", "2025-09-09T12:00", "2025-09-09T13:00"],
        "weather_code": [1, 1, 2, 2, 80],
        "is_day": [1, 1, 1, 1, 1],
        "temperature_2m": [15.9, 17.2, 18.6, 19.1, 19.4],
        "apparent_temperature": [15.1, 16.8, 17.2, 18.0, 18.1],
        "relative_humidity_2m": [73, 65, 53, 53, 52],
        "wind_speed_10m": [7.4, 4.0, 7.6, 6.5, 7.6],
        "precipitation": [0.00, 0.00, 0.00, 1.10, 0.30],
        "precipitation_probability": [0, 0, 0, 30, 15],
        "cloud_cover": [15, 24, 65, 70, 100],
        "uv_index": [2.55, 3.65, 4.50, 4.95, 4.75],
    }
}
