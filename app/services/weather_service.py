"""Weather service for fetching and caching weather forecast data."""

import hashlib
import json
from datetime import datetime, timezone
import re
from typing import Any

import httpx

from app.cache import cache, single_flight
from app.config import settings
from app.http_client import get_http_client
from app.models.weather import WeatherForecast, CurrentWeather, ForecastEntry
from app.parsers.weather_parser import parse_weather_forecast, find_current_forecast

ADM4_PATTERN = re.compile(r"\d{2}\.\d{2}\.\d{2}\.\d{4}")

# Cached in place of a forecast when BMKG answers 404 for a code
NOT_FOUND = {"not_found": True}


class WeatherService:
    """Service for weather forecast operations."""
    
    def __init__(self):
        """Initialize weather service."""
        self.base_url = settings.bmkg_weather_base_url
    
    def _make_cache_key(self, adm4_code: str) -> str:
        """Generate cache key for weather forecast.
        
        Args:
            adm4_code: ADM4 area code
            
        Returns:
            Cache key string
        """
        return f"weather:forecast:{adm4_code}"
    
    async def _fetch_from_bmkg(self, adm4_code: str) -> dict[str, Any]:
        """Fetch weather forecast from BMKG API.
        
        Args:
            adm4_code: ADM4 area code
            
        Returns:
            Parsed JSON response
            
        Raises:
            Exception: On fetch or parse errors
        """
        url = f"{self.base_url}/prakiraan-cuaca"
        client = await get_http_client()
        
        try:
            response = await client.get(url, params={"adm4": adm4_code})
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError:
            raise
        except Exception as e:
            raise Exception(f"Failed to fetch from BMKG: {str(e)}")
    
    async def _get_cached_or_fetch(
        self,
        adm4_code: str,
    ) -> tuple[dict[str, Any], bool]:
        """Get data from cache or fetch from BMKG.
        
        Args:
            adm4_code: ADM4 area code
            
        Returns:
            Tuple of (data, from_cache)
        """
        cache_key = self._make_cache_key(adm4_code)
        
        # Try cache first
        cached = await cache.get(cache_key)
        if cached is not None:
            return self._raise_if_not_found(cached), True

        async with single_flight(cache_key):
            cached = await cache.get(cache_key)
            if cached is not None:
                return self._raise_if_not_found(cached), True

            # Fetch from BMKG
            try:
                data = await self._fetch_from_bmkg(adm4_code)
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    # Remember unknown codes, so repeats do not reach BMKG again
                    await cache.set(cache_key, NOT_FOUND, settings.cache_ttl_weather)
                    self._raise_if_not_found(NOT_FOUND)
                raise Exception(f"Failed to fetch from BMKG: {str(e)}")

            # Store in cache
            await cache.set(cache_key, data, settings.cache_ttl_weather)

        return data, False

    @staticmethod
    def _raise_if_not_found(data: dict[str, Any]) -> dict[str, Any]:
        """Return cached data, or raise if it is the marker for an unknown code."""
        if data == NOT_FOUND:
            raise Exception("BMKG has no forecast for this code (404 Not Found)")
        return data
    
    async def get_forecast(self, adm4_code: str) -> tuple[WeatherForecast, bool, int]:
        """Get weather forecast for an area.
        
        Args:
            adm4_code: ADM4 area code (kelurahan/desa)
            
        Returns:
            Tuple of (forecast, from_cache, ttl)
            
        Raises:
            ValueError: If adm4_code is invalid
            Exception: On fetch or parse errors
        """
        # Validate adm4_code format (should be like "33.26.16.1001")
        if not adm4_code or not isinstance(adm4_code, str):
            raise ValueError("Invalid ADM4 code")
        
        # One canonical spelling per location: anything else would be passed
        # to BMKG and cached under its own key.
        if not ADM4_PATTERN.fullmatch(adm4_code):
            raise ValueError("ADM4 code must look like '33.26.16.1001' (2.2.2.4 digits)")
        
        # Fetch data
        data, from_cache = await self._get_cached_or_fetch(adm4_code)
        
        # Parse forecast
        forecast = parse_weather_forecast(data)
        
        # Get remaining TTL
        cache_key = self._make_cache_key(adm4_code)
        ttl = await cache.ttl(cache_key)
        if ttl < 0:
            ttl = settings.cache_ttl_weather
        
        return forecast, from_cache, ttl
    
    async def get_current(self, adm4_code: str) -> tuple[CurrentWeather, bool, int]:
        """Get current weather for an area.
        
        Args:
            adm4_code: ADM4 area code (kelurahan/desa)
            
        Returns:
            Tuple of (current_weather, from_cache, ttl)
            
        Raises:
            ValueError: If adm4_code is invalid or no current forecast found
            Exception: On fetch or parse errors
        """
        # Get full forecast
        forecast, from_cache, ttl = await self.get_forecast(adm4_code)
        
        # Find current entry
        current_entry = find_current_forecast(forecast)
        if current_entry is None:
            raise ValueError("No current forecast entry found")
        
        current = CurrentWeather(
            location=forecast.location,
            current=current_entry,
        )
        
        return current, from_cache, ttl


# Global service instance
weather_service = WeatherService()
