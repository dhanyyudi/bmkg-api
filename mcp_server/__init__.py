"""BMKG API MCP Server - Model Context Protocol server for BMKG Indonesia data."""

__version__ = "1.0.1"
__tools_count__ = 13
__prompts_count__ = 7
__all__ = ["mcp", "main"]

from mcp_server.mcp_instance import mcp
from mcp_server.server import main
