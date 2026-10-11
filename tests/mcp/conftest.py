"""Test configuration for MCP tests."""

import pytest
from unittest.mock import AsyncMock, patch

from app.cache import InMemoryCache, cache
from mcp_server.client import client


@pytest.fixture(autouse=True)
def fresh_cache():
    """Give each test an empty in-memory cache so cached tool results do not leak."""
    with patch.object(cache, "_use_fallback", True), \
            patch.object(cache, "_fallback", InMemoryCache()):
        yield


@pytest.fixture
def mock_client():
    """Mock BMKG client for testing.

    Tool modules import the shared client instance by name, so patch its
    method rather than the module attribute.
    """
    with patch.object(client, "get", new=AsyncMock()):
        yield client
