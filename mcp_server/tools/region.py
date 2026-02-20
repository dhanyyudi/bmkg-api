"""Region lookup tools for BMKG MCP Server."""

from mcp_server.mcp_instance import mcp
from mcp_server.client import client
from mcp_server.utils import format_error_message
from mcp_server.cache import cached

@mcp.tool()
@cached("region")
async def search_regions(query: str) -> dict:
    """
    Search for regions in Indonesia (provinces, districts, subdistricts, villages).
    
    Args:
        query: Search query (e.g., "tebet", "jakarta", "bandung", "yogyakarta")
    
    Returns matching regions with their codes that can be used with weather tools.
    """
    try:
        return await client.get(
            "/wilayah/search",
            params={"q": query}
        )
    except Exception as e:
        return {"error": format_error_message(e)}

@mcp.tool()
@cached("region")
async def get_provinces() -> dict:
    """
    Get list of all provinces in Indonesia.
    
    Returns all 34 provinces with their codes.
    """
    try:
        return await client.get("/wilayah/provinces")
    except Exception as e:
        return {"error": format_error_message(e)}

@mcp.tool()
@cached("region")
async def get_districts(province_code: str) -> dict:
    """
    Get districts (kabupaten/kota) for a specific province.
    
    Args:
        province_code: Province code (e.g., "31" for DKI Jakarta, "32" for Jawa Barat)
    
    Returns districts within the specified province.
    """
    try:
        return await client.get(
            "/wilayah/districts",
            params={"province": province_code}
        )
    except Exception as e:
        return {"error": format_error_message(e)}

@mcp.tool()
@cached("region")
async def get_subdistricts(district_code: str) -> dict:
    """
    Get subdistricts (kecamatan) for a specific district.
    
    Args:
        district_code: District code (e.g., "31.74" for Jakarta Selatan)
    
    Returns subdistricts within the specified district.
    """
    try:
        return await client.get(
            "/wilayah/subdistricts",
            params={"district": district_code}
        )
    except Exception as e:
        return {"error": format_error_message(e)}

@mcp.tool()
@cached("region")
async def get_villages(subdistrict_code: str) -> dict:
    """
    Get villages (kelurahan/desa) for a specific subdistrict.
    
    Args:
        subdistrict_code: Subdistrict code (e.g., "31.74.04" for Pasar Minggu)
    
    Returns villages within the specified subdistrict with their adm4 codes
    that can be used with weather tools.
    """
    try:
        return await client.get(
            "/wilayah/villages",
            params={"subdistrict": subdistrict_code}
        )
    except Exception as e:
        return {"error": format_error_message(e)}
