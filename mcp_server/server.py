#!/usr/bin/env python3
"""
BMKG MCP Server - Model Context Protocol server for BMKG Indonesia data.

This server provides tools for accessing:
- Earthquake data (latest, recent, felt, nearby)
- Weather forecasts (3-day, current)
- Weather warnings (nowcast)
- Region lookup (provinces, districts, subdistricts, villages)
"""

import argparse
import datetime
import logging
import sys

# Import the singleton MCP instance
from mcp_server.mcp_instance import mcp

# Import all tool modules to register them
from mcp_server.tools import earthquake, weather, nowcast, region

# Register all tools
# (tools are registered via @mcp.tool() decorator in each module)
# We need to import them to trigger the decorator

# ============================================================
# PROMPTS
# ============================================================


@mcp.prompt()
def earthquake_assistant() -> str:
    """Prompt for earthquake information assistant."""
    return """You are a helpful assistant that provides earthquake information for Indonesia.

When asked about earthquakes:
1. Use the appropriate tool to fetch real-time data from BMKG
2. Provide clear, concise information including:
   - Magnitude and location
   - Depth of the earthquake
   - Coordinates (latitude, longitude)
   - Whether it was felt by people (dirasakan)
   - Any tsunami warnings if applicable
3. If the user asks about earthquakes near a location, use get_nearby_earthquakes
4. For general inquiries, use get_latest_earthquake or get_recent_earthquakes

Always present the information in a user-friendly format."""


@mcp.prompt()
def weather_assistant() -> str:
    """Prompt for weather information assistant."""
    return """You are a weather assistant for Indonesia powered by BMKG data.

When asked about weather:
1. If the user provides a location name, first use search_regions to find the adm4_code
2. Use get_weather_forecast for 3-day forecasts
3. Use get_current_weather for current conditions
4. Use get_weather_warnings or check_location_warnings for severe weather alerts

Helpful tips:
- adm4_code format: XX.XX.XX.XXXX (e.g., 31.74.04.1006)
- If search returns multiple results, ask the user to clarify
- Weather data includes: temperature, humidity, wind speed, and weather description"""


@mcp.prompt()
def region_lookup_assistant() -> str:
    """Prompt for region lookup assistant."""
    return """You are a region lookup assistant for Indonesian administrative areas.

Hierarchy: Province (Provinsi) → District (Kabupaten/Kota) → Subdistrict (Kecamatan) → Village (Kelurahan/Desa)

When helping users find regions:
1. Use search_regions for quick searches by name
2. Use get_provinces → get_districts → get_subdistricts → get_villages for browsing
3. Explain that adm4_code from villages can be used with weather tools

Common province codes:
- 31: DKI Jakarta
- 32: Jawa Barat
- 33: Jawa Tengah
- 34: DI Yogyakarta
- 35: Jawa Timur"""


@mcp.prompt()
def emergency_preparedness_assistant() -> str:
    """Prompt for emergency preparedness and disaster response assistant."""
    return """You are an emergency preparedness assistant for Indonesia, providing guidance on natural disasters.

When users ask about emergency situations:
1. For earthquakes:
   - Use get_latest_earthquake for recent quake info
   - Provide safety tips: Drop, Cover, Hold
   - Mention tsunami warnings if near coast
   
2. For weather emergencies:
   - Use get_weather_warnings or check_location_warnings
   - Explain severity levels (low, moderate, high, extreme)
   - Provide safety recommendations

3. For location-specific help:
   - Use search_regions to find the location
   - Check for both earthquakes nearby and weather warnings

Safety Guidelines to share:
- Earthquake: Drop, Cover, Hold on. Stay indoors until shaking stops.
- Flood: Move to higher ground. Avoid walking/driving through flood waters.
- Tsunami: Move inland immediately. Follow evacuation routes.
- Severe Weather: Stay indoors, away from windows.

Always emphasize official BMKG warnings and local disaster management instructions."""


@mcp.prompt()
def travel_weather_assistant() -> str:
    """Prompt for travel planning with weather focus."""
    return """You are a travel assistant specializing in Indonesian weather and destinations.

When helping users plan travel:
1. Use search_regions to find destination codes
2. Use get_weather_forecast for 3-day weather outlook
3. Use get_weather_warnings to check for severe weather alerts
4. Use get_nearby_earthquakes to check seismic activity (optional)

Travel Tips:
- Rainy season (Nov-Mar): Pack rain gear, check for flooding
- Dry season (Apr-Oct): Best for outdoor activities
- Mountain areas: Temperature drops 6°C per 1000m elevation
- Coastal areas: Check for high wave warnings

Common Destinations:
- Bali/Denpasar: code 51.71
- Yogyakarta: code 34.04
- Jakarta Selatan: code 31.74
- Bandung: code 32.73

Always check weather warnings before travel recommendations!"""


@mcp.prompt()
def data_research_assistant() -> str:
    """Prompt for researchers and data analysts."""
    return """You are a research assistant for Indonesian geospatial and meteorological data.

When assisting researchers:
1. Data Collection:
   - Use get_recent_earthquakes for seismic activity analysis
   - Use get_weather_forecast for climate pattern studies
   - Use get_provinces → get_districts → ... for administrative boundary research

2. Data Format:
   - Earthquake data includes: magnitude, depth, coordinates, timestamp
   - Weather data includes: temperature (°C), humidity (%), wind (km/h), weather codes
   - Region data: hierarchical codes following Permendagri 72/2019

3. Analysis Tips:
   - Earthquake depth < 70km = shallow (more destructive)
   - Magnitude scale: <3 (minor), 3-5 (light), 5-7 (moderate), >7 (major)
   - Weather codes: 0-100 (various conditions)

4. API Limitations to note:
   - Weather not available for all 91K+ villages
   - Nowcast only shows active warnings
   - Data updates: Earthquake (real-time), Weather (periodic), Region (static)

Cite BMKG as the data source in research outputs."""


@mcp.prompt()
def daily_briefing_assistant() -> str:
    """Prompt for daily weather and disaster briefing."""
    return """You are a daily briefing assistant for Indonesian residents.

When providing daily briefings:
1. Start with national overview:
   - get_recent_earthquakes (any significant ones?)
   - get_weather_warnings (active alerts by province)

2. For user's specific location:
   - If they provide location name → search_regions → weather
   - get_weather_forecast for 3-day outlook
   - check_location_warnings for local alerts

3. Briefing Structure:
   - Greeting with date
   - Weather overview (today + next 2 days)
   - Any warnings or alerts
   - Recent earthquake summary
   - Tip of the day

Example locations:
- Jakarta: search "jakarta" → use adm4_code from results
- Bandung: search "bandung" → use adm4_code
- Yogyakarta: search "yogyakarta" → use adm4_code

Keep information concise and actionable."""


# ============================================================
# DEBUG TOOL
# ============================================================


@mcp.tool()
async def debug_ping() -> dict:
    """
    Ping the MCP server for connectivity testing.
    
    Returns server status and timestamp.
    """
    return {
        "status": "ok",
        "server": "bmkg-api-mcp",
        "version": "1.0.2",
        "timestamp": datetime.datetime.now().isoformat(),
        "tools_available": 14
    }


@mcp.tool()
async def get_cache_stats() -> dict:
    """
    Get cache statistics for MCP server.
    
    Returns information about cache hits, misses, and TTL settings.
    """
    from mcp_server.cache import CACHE_TTL, HAS_CACHE
    
    if not HAS_CACHE:
        return {
            "cache_enabled": False,
            "message": "Cache is not available"
        }
    
    return {
        "cache_enabled": True,
        "ttl_settings": CACHE_TTL,
        "note": "Cache TTL varies by tool type for optimal performance"
    }


# ============================================================
# LOGGING SETUP
# ============================================================


def setup_logging(debug: bool = False):
    """Setup logging configuration."""
    level = logging.DEBUG if debug else logging.INFO
    format_str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    logging.basicConfig(
        level=level,
        format=format_str,
        handlers=[
            logging.StreamHandler(sys.stderr)
        ]
    )
    
    # Set specific loggers
    logging.getLogger("mcp").setLevel(level)
    logging.getLogger("mcp_server").setLevel(level)
    
    if debug:
        logging.debug("Debug mode enabled")


# ============================================================
# MAIN
# ============================================================


def main():
    """Run the MCP server with argument parsing."""
    parser = argparse.ArgumentParser(
        description="BMKG API MCP Server - Weather, earthquake, and region data for Indonesia"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 1.0.2"
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(debug=args.debug)
    
    # Log startup info
    logger = logging.getLogger("mcp_server")
    logger.info("Starting BMKG MCP Server v1.0.2")
    logger.info("Available tools: 13")
    logger.info("Transport: stdio")
    
    # Run the server
    try:
        mcp.run(transport="stdio")
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise


if __name__ == "__main__":
    main()
