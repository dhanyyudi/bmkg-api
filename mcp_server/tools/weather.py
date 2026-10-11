"""Weather tools for BMKG MCP Server."""

from typing import Annotated

from pydantic import Field

from mcp_server.envelope import ToolResponse, call_api
from mcp_server.mcp_instance import READ_ONLY, mcp

Adm4Code = Annotated[
    str,
    Field(
        description="Village-level (adm4) region code, e.g. '31.74.04.1006'. Find it with search_regions.",
        pattern=r"^\d{2}\.\d{2}\.\d{2}\.\d{4}$",
    ),
]

NO_FORECAST = (
    "BMKG has no forecast for that code. Use search_regions to confirm the code, "
    "or try a neighbouring village from get_villages."
)


@mcp.tool(annotations={"title": "3-day weather forecast", **READ_ONLY})
async def get_weather_forecast(adm4_code: Adm4Code) -> ToolResponse:
    """Get the 3-day weather forecast for one village (kelurahan/desa) in Indonesia.

    Returns entries every 3 hours with temperature (°C), humidity (%), weather
    condition in Indonesian and English, wind and cloud cover, grouped by day.
    Each entry has both `local_datetime` and `utc_datetime`. Use
    get_current_weather if only the present conditions are needed.
    """
    return await call_api(
        "get_weather_forecast", f"/weather/{adm4_code}", cache_type="weather", not_found=NO_FORECAST
    )


@mcp.tool(annotations={"title": "Current weather", **READ_ONLY})
async def get_current_weather(adm4_code: Adm4Code) -> ToolResponse:
    """Get the weather right now for one village (kelurahan/desa) in Indonesia.

    Returns the forecast entry closest to the current time: temperature (°C),
    humidity (%), weather condition, wind and cloud cover. This is BMKG's
    forecast for the current 3-hour slot, not a live station reading.
    """
    return await call_api(
        "get_current_weather", f"/weather/{adm4_code}/current", cache_type="weather", not_found=NO_FORECAST
    )
