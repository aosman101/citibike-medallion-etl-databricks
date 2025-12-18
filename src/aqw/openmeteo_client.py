from __future__ import annotations
import requests
from typing import Any

HISTORICAL_FORECAST_HOST = "https://historical-forecast-api.open-meteo.com/v1/forecast"

def hourly_weather(lat: float, lon: float, start_date: str, end_date: str) -> dict[str, Any]:
    """
    Fetch hourly weather time series between start_date and end_date (YYYY-MM-DD).
    """
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": "temperature_2m,precipitation,wind_speed_10m",
        "timezone": "UTC",
    }
    r = requests.get(HISTORICAL_FORECAST_HOST, params=params, timeout=30)
    r.raise_for_status()
    return r.json()

