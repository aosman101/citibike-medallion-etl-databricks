from __future__ import annotations

import os
from typing import Any

import requests

BASE_URL = "https://api.openaq.org/v3"


def _headers() -> dict[str, str]:
    api_key = os.getenv("OPENAQ_API_KEY", "")
    return {"X-API-Key": api_key} if api_key else {}


def list_locations_near(lat: float, lon: float, radius_m: int = 8000, limit: int = 25) -> list[dict[str, Any]]:
    """
    Uses /v3/locations with coordinates+radius to find nearby monitoring locations.
    The response includes sensors and their parameters.
    """
    r = requests.get(
        f"{BASE_URL}/locations",
        params={"coordinates": f"{lat},{lon}", "radius": radius_m, "limit": limit},
        headers=_headers(),
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["results"]


def sensor_hourly(sensor_id: int, datetime_from: str, datetime_to: str, limit: int = 1000) -> list[dict[str, Any]]:
    """
    Calls the hourly aggregation endpoint for a sensor over a bounded time range.
    """
    r = requests.get(
        f"{BASE_URL}/sensors/{sensor_id}/measurements/hourly",
        params={"datetime_from": datetime_from, "datetime_to": datetime_to, "limit": limit},
        headers=_headers(),
        timeout=30,
    )
    r.raise_for_status()
    return r.json()["results"]
