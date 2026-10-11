"""MCP Instance - Singleton FastMCP instance for BMKG API."""

from fastmcp import FastMCP

INSTRUCTIONS = """Weather forecasts, earthquakes, severe weather warnings and administrative \
regions of Indonesia, from BMKG open data. All tools are read-only.

Every tool returns the same envelope: check `status`. On "success" read `data`; on "error" \
read `error.code` (INVALID_ARGUMENT, NOT_FOUND, RATE_LIMITED, UPSTREAM_UNAVAILABLE, \
INTERNAL_ERROR) and `error.message`. Cite `meta.source` when reporting results.

Weather tools need an adm4 code (village level, like 31.74.04.1006). Get one with \
search_regions, or walk get_provinces → get_districts → get_subdistricts → get_villages. \
Times in results are UTC unless a field name says local."""

# Singleton FastMCP instance
mcp = FastMCP("bmkg-api", instructions=INSTRUCTIONS)

# Every tool only reads public data from an external service.
READ_ONLY = {"readOnlyHint": True, "idempotentHint": True, "openWorldHint": True}
