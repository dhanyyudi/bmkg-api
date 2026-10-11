"""Tests for Cache-Control headers and rate limit keying."""

import pytest
from fastapi.testclient import TestClient
from starlette.requests import Request

from app.cache_headers import cache_control_for
from app.config import settings
from app.dependencies import get_client_ip
from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def make_request(headers: dict[str, str] | None = None) -> Request:
    """Build a bare request coming from the proxy address 10.0.0.1."""
    raw_headers = [(k.lower().encode(), v.encode()) for k, v in (headers or {}).items()]
    return Request({"type": "http", "headers": raw_headers, "client": ("10.0.0.1", 1234)})


class TestCacheControlFor:
    """Test Cache-Control value selection."""

    @pytest.mark.parametrize("path,ttl", [
        ("/v1/earthquake/latest", settings.cache_ttl_earthquake_latest),
        ("/v1/earthquake/recent", settings.cache_ttl_earthquake_list),
        ("/v1/earthquake/nearby", settings.cache_ttl_earthquake_list),
        ("/v1/nowcast", settings.cache_ttl_nowcast),
        ("/v1/nowcast/CBT20260216004", settings.cache_ttl_nowcast),
        ("/v1/weather/31.74.04.1006", settings.cache_ttl_weather),
        ("/v1/weather/31.74.04.1006/current", settings.cache_ttl_weather),
        ("/v1/wilayah/provinces", settings.cache_ttl_wilayah),
    ])
    def test_success_uses_endpoint_ttl(self, path, ttl):
        """Test each endpoint gets its configured TTL."""
        assert cache_control_for(path, 200) == f"public, max-age={ttl}"

    def test_success_follows_remaining_ttl(self):
        """Test max-age shrinks to the time left on the server-side cache entry."""
        assert cache_control_for("/v1/weather/31.74.04.1006", 200, "42") == "public, max-age=42"

    def test_remaining_ttl_never_exceeds_endpoint_ttl(self):
        """Test a larger remaining TTL does not extend the configured TTL."""
        ttl = settings.cache_ttl_earthquake_latest
        assert cache_control_for("/v1/earthquake/latest", 200, str(ttl + 500)) == f"public, max-age={ttl}"

    @pytest.mark.parametrize("status_code", [400, 404, 422])
    def test_client_errors_cached_briefly(self, status_code):
        """Test client errors are cacheable for a short time."""
        assert cache_control_for("/v1/weather/99.99.99.9999", status_code) == "public, max-age=60"

    @pytest.mark.parametrize("status_code", [429, 500, 502, 503])
    def test_rate_limit_and_server_errors_not_cached(self, status_code):
        """Test responses that must not be shared between clients."""
        assert cache_control_for("/v1/earthquake/latest", status_code) == "no-store"

    @pytest.mark.parametrize("path", ["/health", "/ready"])
    def test_health_not_cached(self, path):
        """Test health endpoints are never cached."""
        assert cache_control_for(path, 200) == "no-store"

    @pytest.mark.parametrize("path", ["/redoc", "/openapi.json", "/logo.svg"])
    def test_other_paths_untouched(self, path):
        """Test non-API paths keep their own caching behaviour."""
        assert cache_control_for(path, 200) is None

    @pytest.mark.parametrize("path", ["/", "/docs/", "/self-host/", "/404.html"])
    def test_pages_are_revalidated(self, path):
        """Test a page is never reused across a deploy without checking."""
        assert cache_control_for(path, 200) == "no-cache"

    def test_hashed_build_files_are_immutable(self):
        """Test content-hashed build output is cached for good."""
        value = cache_control_for("/_app/immutable/nodes/2.CQZi2gHX.js", 200)
        assert value == "public, max-age=31536000, immutable"

    def test_missing_build_file_is_not_cached(self):
        """Test a 404 for a build file is not given the immutable policy."""
        assert cache_control_for("/_app/immutable/nodes/gone.js", 404) is None


class TestCacheControlMiddleware:
    """Test headers on real responses."""

    def test_wilayah_response_is_cacheable(self, client):
        """Test a successful API response carries Cache-Control."""
        response = client.get("/v1/wilayah/provinces")
        assert response.status_code == 200
        assert response.headers["Cache-Control"] == f"public, max-age={settings.cache_ttl_wilayah}"

    def test_cors_header_present_without_origin(self, client):
        """Test a cacheable response allows any origin even if the request sent none."""
        response = client.get("/v1/wilayah/provinces")
        assert response.headers["Access-Control-Allow-Origin"] == "*"

    def test_cors_header_same_for_browser_request(self, client):
        """Test a browser request gets the same shareable CORS answer."""
        response = client.get("/v1/wilayah/provinces", headers={"Origin": "https://example.com"})
        assert response.headers["Access-Control-Allow-Origin"] == "*"

    def test_validation_error_cached_briefly(self, client):
        """Test a rejected request is cacheable for a short time."""
        response = client.get("/v1/wilayah/districts")
        assert response.status_code == 422
        assert response.headers["Cache-Control"] == "public, max-age=60"

    def test_health_is_not_cacheable(self, client):
        """Test health endpoint is never cached."""
        response = client.get("/health")
        assert response.headers["Cache-Control"] == "no-store"


class TestClientIp:
    """Test rate limit key selection."""

    def test_defaults_to_socket_address(self, monkeypatch):
        """Test a forwarded header is ignored unless configured."""
        monkeypatch.setattr(settings, "client_ip_header", "")
        request = make_request({"CF-Connecting-IP": "203.0.113.7"})
        assert get_client_ip(request) == "10.0.0.1"

    def test_reads_configured_header(self, monkeypatch):
        """Test the configured header identifies the visitor behind the proxy."""
        monkeypatch.setattr(settings, "client_ip_header", "CF-Connecting-IP")
        request = make_request({"CF-Connecting-IP": "203.0.113.7"})
        assert get_client_ip(request) == "203.0.113.7"

    def test_falls_back_when_header_missing(self, monkeypatch):
        """Test requests that bypass the proxy are keyed by socket address."""
        monkeypatch.setattr(settings, "client_ip_header", "CF-Connecting-IP")
        assert get_client_ip(make_request()) == "10.0.0.1"
