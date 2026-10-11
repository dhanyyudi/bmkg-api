"""Nowcast (weather warnings) tools for BMKG MCP Server."""

from typing import Annotated, Literal

from pydantic import Field

from mcp_server.envelope import ToolResponse, call_api
from mcp_server.mcp_instance import READ_ONLY, mcp

Language = Annotated[Literal["id", "en"], Field(description="Language of the warning text: Indonesian or English")]


@mcp.tool(annotations={"title": "Active weather warnings", **READ_ONLY})
async def get_weather_warnings(language: Language = "id") -> ToolResponse:
    """List BMKG's currently active severe weather warnings (nowcast), one per province.

    Each item has the province, a description of the hazard, the affected
    areas and the time it was issued. An empty list means no province has an
    active warning. Use check_location_warnings to ask about one place.
    """
    return await call_api("get_weather_warnings", "/nowcast", {"lang": language}, cache_type="nowcast")


@mcp.tool(annotations={"title": "Weather warnings for a place", **READ_ONLY})
async def check_location_warnings(
    location: Annotated[
        str,
        Field(
            description="Name of a kecamatan, city or regency as BMKG writes it, e.g. 'Wiradesa' or 'Jakarta Selatan'",
            min_length=2,
            max_length=100,
        ),
    ],
    language: Language = "id",
) -> ToolResponse:
    """Check whether any active severe weather warning mentions a place.

    Matches the name against the text of every active warning, so spelling
    matters: prefer the Indonesian place name. `has_warnings` is false when no
    active warning mentions it, which is not a forecast of good weather.
    """
    return await call_api(
        "check_location_warnings",
        "/nowcast/check",
        {"location": location, "lang": language},
        cache_type="nowcast",
    )
