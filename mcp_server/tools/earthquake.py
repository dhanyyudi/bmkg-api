"""Earthquake tools for BMKG MCP Server."""

from mcp_server.mcp_instance import mcp
from mcp_server.client import client
from mcp_server.utils import format_error_message, validate_coordinates, validate_radius
from mcp_server.cache import cached


@mcp.tool()
@cached("earthquake")
async def get_latest_earthquake() -> dict:
    """
    Get the latest earthquake data from BMKG Indonesia.
    
    Returns information about the most recent earthquake including:
    - Magnitude and location
    - Depth and coordinates
    - Time and date
    - Whether it was felt by people
    """
    try:
        return await client.get("/earthquake/latest")
    except Exception as e:
        return {"error": format_error_message(e)}


@mcp.tool()
@cached("earthquake")
async def get_recent_earthquakes() -> dict:
    """
    Get recent earthquakes with magnitude 5.0+ from BMKG Indonesia.
    
    Returns a list of significant earthquakes that occurred recently.
    """
    try:
        return await client.get("/earthquake/recent")
    except Exception as e:
        return {"error": format_error_message(e)}


@mcp.tool()
@cached("earthquake")
async def get_felt_earthquakes() -> dict:
    """
    Get earthquakes that were felt by people in Indonesia.
    
    Returns a list of earthquakes with felt reports from the public.
    """
    try:
        return await client.get("/earthquake/felt")
    except Exception as e:
        return {"error": format_error_message(e)}


@mcp.tool()
@cached("earthquake")
async def get_nearby_earthquakes(
    latitude: float,
    longitude: float,
    radius_km: int = 100
) -> dict:
    """
    Find earthquakes near specific coordinates.
    
    Args:
        latitude: Latitude coordinate (e.g., -6.2088 for Jakarta)
        longitude: Longitude coordinate (e.g., 106.8456 for Jakarta)
        radius_km: Search radius in kilometers (default: 100, max: 500)
    
    Returns earthquakes within the specified radius.
    """
    if not validate_coordinates(latitude, longitude):
        return {"error": "Koordinat tidak valid. Latitude: -90 sampai 90, Longitude: -180 sampai 180."}
    
    radius_km = validate_radius(radius_km)
    
    try:
        return await client.get(
            "/earthquake/nearby",
            params={"lat": latitude, "lon": longitude, "radius_km": radius_km}
        )
    except Exception as e:
        return {"error": format_error_message(e)}
