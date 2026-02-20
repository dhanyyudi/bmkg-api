"""Weather tools for BMKG MCP Server."""

from mcp_server.mcp_instance import mcp
from mcp_server.client import client
from mcp_server.utils import format_error_message
from mcp_server.cache import cached


@mcp.tool()
@cached("weather")
async def get_weather_forecast(adm4_code: str) -> dict:
    """
    Get 3-day weather forecast for a specific location in Indonesia.
    
    Args:
        adm4_code: Administrative level 4 code (kelurahan/desa code)
                  Example: "31.74.04.1006" for Pejaten Barat, Jakarta Selatan
                  Use search_regions to find the code for your location.
    
    Returns weather forecast including temperature, humidity, wind, and weather description.
    """
    try:
        return await client.get(f"/weather/{adm4_code}")
    except Exception as e:
        return {"error": format_error_message(e)}


@mcp.tool()
@cached("weather")
async def get_current_weather(adm4_code: str) -> dict:
    """
    Get current weather for a specific location in Indonesia.
    
    Args:
        adm4_code: Administrative level 4 code (kelurahan/desa code)
                  Example: "31.74.04.1006" for Pejaten Barat, Jakarta Selatan
    
    Returns current weather conditions including temperature, humidity, and weather description.
    """
    try:
        return await client.get(f"/weather/{adm4_code}/current")
    except Exception as e:
        return {"error": format_error_message(e)}
