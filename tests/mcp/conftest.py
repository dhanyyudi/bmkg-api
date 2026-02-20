"""Test configuration for MCP tests."""

import pytest
from unittest.mock import AsyncMock, patch


@pytest.fixture
def mock_client():
    """Mock BMKG client for testing."""
    with patch("mcp_server.client.client") as mock:
        mock.get = AsyncMock()
        yield mock
