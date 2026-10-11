"""Region lookup tools for BMKG MCP Server."""

from typing import Annotated

from pydantic import Field

from mcp_server.envelope import ToolResponse, call_api
from mcp_server.mcp_instance import READ_ONLY, mcp


@mcp.tool(annotations={"title": "Search regions by name", **READ_ONLY})
async def search_regions(
    query: Annotated[
        str,
        Field(description="Part of a region name, e.g. 'tebet' or 'pekalongan'", min_length=2, max_length=100),
    ],
    limit: Annotated[int, Field(description="Maximum number of results", ge=1, le=100)] = 20,
) -> ToolResponse:
    """Search Indonesian administrative regions by name, at every level.

    Returns the code, level (province, district, subdistrict or village) and
    full path of each match. Weather tools need a village-level code (four
    parts, like 31.74.04.1006): if a match is a higher level, list its villages
    with get_villages.
    """
    return await call_api(
        "search_regions", "/wilayah/search", {"q": query, "limit": limit}, cache_type="region"
    )


@mcp.tool(annotations={"title": "List provinces", **READ_ONLY})
async def get_provinces() -> ToolResponse:
    """List the provinces of Indonesia with their 2-digit codes.

    Starting point for browsing down to a village. The list follows
    Permendagri 72/2019 (34 provinces), so the provinces created in Papua
    after 2022 are not listed.
    """
    return await call_api("get_provinces", "/wilayah/provinces", cache_type="region")


@mcp.tool(annotations={"title": "List districts in a province", **READ_ONLY})
async def get_districts(
    province_code: Annotated[
        str, Field(description="2-digit province code, e.g. '31' for DKI Jakarta", pattern=r"^\d{2}$")
    ],
) -> ToolResponse:
    """List the districts (kabupaten and kota) of one province."""
    return await call_api(
        "get_districts",
        "/wilayah/districts",
        {"province": province_code},
        cache_type="region",
        not_found="No province has that code. Use get_provinces to list valid codes.",
    )


@mcp.tool(annotations={"title": "List subdistricts in a district", **READ_ONLY})
async def get_subdistricts(
    district_code: Annotated[
        str, Field(description="District code, e.g. '31.74' for Jakarta Selatan", pattern=r"^\d{2}\.\d{2}$")
    ],
) -> ToolResponse:
    """List the subdistricts (kecamatan) of one district."""
    return await call_api(
        "get_subdistricts",
        "/wilayah/subdistricts",
        {"district": district_code},
        cache_type="region",
        not_found="No district has that code. Use get_districts to list valid codes.",
    )


@mcp.tool(annotations={"title": "List villages in a subdistrict", **READ_ONLY})
async def get_villages(
    subdistrict_code: Annotated[
        str,
        Field(description="Subdistrict code, e.g. '31.74.04' for Pasar Minggu", pattern=r"^\d{2}\.\d{2}\.\d{2}$"),
    ],
) -> ToolResponse:
    """List the villages (kelurahan and desa) of one subdistrict.

    Each village code is an adm4 code that the weather tools accept.
    """
    return await call_api(
        "get_villages",
        "/wilayah/villages",
        {"subdistrict": subdistrict_code},
        cache_type="region",
        not_found="No subdistrict has that code. Use get_subdistricts to list valid codes.",
    )
