"""Earthquake tools for BMKG MCP Server."""

from typing import Annotated

from pydantic import Field

from mcp_server.envelope import ToolResponse, call_api
from mcp_server.mcp_instance import READ_ONLY, mcp


@mcp.tool(annotations={"title": "Latest earthquake", **READ_ONLY})
async def get_latest_earthquake() -> ToolResponse:
    """Get the single most recent earthquake recorded by BMKG in Indonesia.

    Returns magnitude, depth, coordinates, region, time (UTC), tsunami potential,
    felt reports and a shakemap image URL. Use this for "was there just an
    earthquake?"; use get_recent_earthquakes for a list.
    """
    return await call_api("get_latest_earthquake", "/earthquake/latest", cache_type="earthquake")


@mcp.tool(annotations={"title": "Recent strong earthquakes (M 5.0+)", **READ_ONLY})
async def get_recent_earthquakes() -> ToolResponse:
    """List the 15 most recent earthquakes of magnitude 5.0 or higher in Indonesia.

    Newest first. Smaller earthquakes are not included: use get_felt_earthquakes
    for those that people reported feeling.
    """
    return await call_api("get_recent_earthquakes", "/earthquake/recent", cache_type="earthquake")


@mcp.tool(annotations={"title": "Recently felt earthquakes", **READ_ONLY})
async def get_felt_earthquakes() -> ToolResponse:
    """List the 15 most recent earthquakes that people in Indonesia reported feeling.

    Includes small earthquakes and, in `felt_report`, the places and intensity
    (MMI) where each was felt.
    """
    return await call_api("get_felt_earthquakes", "/earthquake/felt", cache_type="earthquake")


@mcp.tool(annotations={"title": "Earthquakes near a point", **READ_ONLY})
async def get_nearby_earthquakes(
    latitude: Annotated[float, Field(description="Latitude in decimal degrees, e.g. -6.2088 for Jakarta", ge=-90, le=90)],
    longitude: Annotated[float, Field(description="Longitude in decimal degrees, e.g. 106.8456 for Jakarta", ge=-180, le=180)],
    radius_km: Annotated[int, Field(description="Search radius in kilometers", ge=1, le=500)] = 100,
) -> ToolResponse:
    """Find recent earthquakes within a radius of a coordinate, nearest first.

    Searches BMKG's recent and felt lists only, so an empty result means
    "none among the latest recorded", not "none ever". Each result includes
    `distance_km`.
    """
    return await call_api(
        "get_nearby_earthquakes",
        "/earthquake/nearby",
        {"lat": latitude, "lon": longitude, "radius_km": radius_km},
        cache_type="earthquake",
    )
