#!/usr/bin/env python3
"""
BMKG MCP HTTP Server - Streamable HTTP Transport.

This server provides MCP tools over HTTP for remote access.
Designed for deployment behind Cloudflare Tunnel.
"""

import argparse
import logging
import os
import sys

# Setup logging first
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("bmkg-mcp-http")

# Import the existing MCP instance (tools already registered)
from mcp_server.mcp_instance import mcp

# Import tool modules to ensure they're registered
from mcp_server.tools import earthquake, weather, nowcast, region

from starlette.requests import Request
from starlette.responses import PlainTextResponse

# Nothing on this host is a page: it only speaks MCP. Without this file search
# engines keep fetching /mcp and report the 4xx answer as an indexing problem.
ROBOTS_TXT = "User-agent: *\nDisallow: /\n"


@mcp.custom_route("/robots.txt", methods=["GET"])
async def robots_txt(request: Request) -> PlainTextResponse:
    return PlainTextResponse(ROBOTS_TXT, headers={"Cache-Control": "public, max-age=86400"})


def main():
    """Run the MCP HTTP server with streamable HTTP transport."""
    parser = argparse.ArgumentParser(
        description="BMKG MCP HTTP Server - Weather, earthquake, and region data"
    )
    parser.add_argument(
        "--host",
        default=os.getenv("HOST", "0.0.0.0"),
        help="Server host (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("PORT", "8000")),
        help="Server port (default: 8000)"
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging"
    )
    
    args = parser.parse_args()
    
    # Set log level
    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")
    
    # Update server name and settings for HTTP
    mcp._name = "bmkg-api-http"
    mcp._instructions = "BMKG Indonesia MCP Server - Weather, Earthquake, and Region Data"
    
    logger.info("🚀 BMKG MCP HTTP Server starting up")
    logger.info(f"📦 Server: {mcp._name}")
    logger.info(f"🔧 Transport: Streamable HTTP")
    logger.info(f"🌐 Host: {args.host}:{args.port}")
    
    # Run with streamable HTTP transport
    # This uses the existing mcp instance with all tools already registered
    mcp.run(
        transport="streamable-http",
        host=args.host,
        port=args.port,
        path="/mcp"
    )


if __name__ == "__main__":
    main()
