"""Tests for robots.txt: the website is crawlable, the JSON endpoints are not."""

from fastapi.testclient import TestClient

from app.main import app


def test_robots_txt_keeps_crawlers_off_the_api():
    """Test the API host serves robots.txt that closes /v1/ and leaves the website open."""
    response = TestClient(app).get("/robots.txt")

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/plain")
    lines = response.text.splitlines()
    assert "User-agent: *" in lines
    assert "Allow: /" in lines
    assert "Disallow: /v1/" in lines
    assert "Disallow: /" not in lines


def test_mcp_host_closes_everything():
    """Test the MCP host tells crawlers that nothing on it is a page."""
    from mcp_server.http_server import ROBOTS_TXT

    assert ROBOTS_TXT.splitlines() == ["User-agent: *", "Disallow: /"]
