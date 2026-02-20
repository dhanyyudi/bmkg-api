"""Nowcast (weather warnings) tools for BMKG MCP Server."""

from mcp_server.mcp_instance import mcp
from mcp_server.client import client
from mcp_server.utils import format_error_message
from mcp_server.cache import cached

@mcp.tool()
@cached("nowcast")
async def get_weather_warnings() -> dict:
    """
    Get active weather warnings (nowcast) by province from BMKG.
    
    Returns current severe weather alerts including:
    - Heavy rain warnings
    - Strong wind alerts
    - High wave warnings
    - Hot temperature alerts
    """
    try:
        return await client.get("/nowcast")
    except Exception as e:
        return {"error": format_error_message(e)}

@mcp.tool()
@cached("nowcast")
async def check_location_warnings(location: str) -> dict:
    """
    Check weather warnings for a specific location.
    
    Args:
        location: Location name to check (e.g., "Jakarta", "Bandung", "Surabaya")
    
    Returns active weather warnings affecting the specified location.
    """
    try:
        return await client.get(
            "/nowcast/check",
            params={"location": location}
        )
    except Exception as e:
        return {"error": format_error_message(e)}
