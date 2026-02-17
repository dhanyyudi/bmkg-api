"""Pydantic models for the BMKG API."""

from app.models.earthquake import (
    Earthquake,
    EarthquakeWithDistance,
    EarthquakeListMeta,
    NearbyEarthquakeMeta,
)
from app.models.weather import (
    Location,
    ForecastEntry,
    ForecastDay,
    WeatherForecast,
    CurrentWeather,
    WeatherForecastMeta,
)
from app.models.wilayah import (
    Wilayah,
    WilayahLevel,
    WilayahSearchResult,
    WilayahListResponse,
    WilayahSearchResponse,
)
from app.models.nowcast import (
    Area,
    Warning,
    ActiveProvince,
    NowcastDetailResponse,
    LocationCheckResult,
    NowcastMeta,
)
from app.models.enums import (
    Severity,
    Urgency,
    Certainty,
    WeatherCode,
    WEATHER_CODE_NAMES,
)
from app.models.responses import (
    Meta,
    APIResponse,
    ErrorResponse,
    HealthResponse,
    ReadinessResponse,
)

__all__ = [
    # Earthquake
    "Earthquake",
    "EarthquakeWithDistance",
    "EarthquakeListMeta",
    "NearbyEarthquakeMeta",
    # Weather
    "Location",
    "ForecastEntry",
    "ForecastDay",
    "WeatherForecast",
    "CurrentWeather",
    "WeatherForecastMeta",
    # Wilayah
    "Wilayah",
    "WilayahLevel",
    "WilayahSearchResult",
    "WilayahListResponse",
    "WilayahSearchResponse",
    # Nowcast
    "Area",
    "Warning",
    "ActiveProvince",
    "NowcastDetailResponse",
    "LocationCheckResult",
    "NowcastMeta",
    # Enums
    "Severity",
    "Urgency",
    "Certainty",
    "WeatherCode",
    "WEATHER_CODE_NAMES",
    # Responses
    "Meta",
    "APIResponse",
    "ErrorResponse",
    "HealthResponse",
    "ReadinessResponse",
]
