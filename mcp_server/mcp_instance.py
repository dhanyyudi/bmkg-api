"""MCP Instance - Singleton FastMCP instance for BMKG API."""

from mcp.server.fastmcp import FastMCP

# Singleton FastMCP instance
mcp = FastMCP("bmkg-api")
