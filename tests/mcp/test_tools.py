"""Tests for MCP tools: routing, response envelope and error codes."""

import httpx
import pytest
from fastmcp.exceptions import ToolError

from mcp_server import __version__

API_PAYLOAD = {
    "data": {"magnitude": 5.4, "region": "18 km TimurLaut Pekalongan"},
    "meta": {"fetched_at": "2026-02-16T08:30:00Z", "cache_ttl": 60, "count": 1},
    "attribution": "BMKG (Badan Meteorologi, Klimatologi, dan Geofisika)",
}


def http_error(status: int) -> httpx.HTTPStatusError:
    """Build the error httpx raises for an API response with this status."""
    request = httpx.Request("GET", "http://api.test/v1/secret-internal-path")
    return httpx.HTTPStatusError(f"{status} error", request=request, response=httpx.Response(status, request=request))


async def call(mcp_client, name: str, arguments: dict | None = None) -> dict:
    """Call a tool and return its envelope."""
    result = await mcp_client.call_tool(name, arguments or {})
    return result.structured_content


class TestRouting:
    """Test each tool asks the API for the right thing."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("tool,arguments,endpoint,params", [
        ("get_latest_earthquake", {}, "/earthquake/latest", None),
        ("get_recent_earthquakes", {}, "/earthquake/recent", None),
        ("get_felt_earthquakes", {}, "/earthquake/felt", None),
        ("get_nearby_earthquakes", {"latitude": -6.2, "longitude": 106.8},
         "/earthquake/nearby", {"lat": -6.2, "lon": 106.8, "radius_km": 100}),
        ("get_weather_forecast", {"adm4_code": "31.74.04.1006"}, "/weather/31.74.04.1006", None),
        ("get_current_weather", {"adm4_code": "31.74.04.1006"}, "/weather/31.74.04.1006/current", None),
        ("get_weather_warnings", {}, "/nowcast", {"lang": "id"}),
        ("get_weather_warnings", {"language": "en"}, "/nowcast", {"lang": "en"}),
        ("check_location_warnings", {"location": "Wiradesa"}, "/nowcast/check", {"location": "Wiradesa", "lang": "id"}),
        ("search_regions", {"query": "tebet"}, "/wilayah/search", {"q": "tebet", "limit": 20}),
        ("get_provinces", {}, "/wilayah/provinces", None),
        ("get_districts", {"province_code": "31"}, "/wilayah/districts", {"province": "31"}),
        ("get_subdistricts", {"district_code": "31.74"}, "/wilayah/subdistricts", {"district": "31.74"}),
        ("get_villages", {"subdistrict_code": "31.74.04"}, "/wilayah/villages", {"subdistrict": "31.74.04"}),
    ])
    async def test_tool_calls_endpoint(self, mcp_client, mock_client, tool, arguments, endpoint, params):
        """Test the tool requests its endpoint with the expected parameters."""
        mock_client.get.return_value = API_PAYLOAD

        envelope = await call(mcp_client, tool, arguments)

        mock_client.get.assert_awaited_once_with(endpoint, params=params)
        assert envelope["status"] == "success"
        assert envelope["meta"]["operation"] == tool


class TestSuccessEnvelope:
    """Test the shape of a successful result."""

    @pytest.mark.asyncio
    async def test_envelope_fields(self, mcp_client, mock_client):
        """Test data, provenance and timing are reported."""
        mock_client.get.return_value = API_PAYLOAD

        envelope = await call(mcp_client, "get_latest_earthquake")

        assert envelope["data"] == API_PAYLOAD["data"]
        assert envelope["error"] is None
        meta = envelope["meta"]
        assert meta["tool_version"] == __version__
        assert meta["source"] == API_PAYLOAD["attribution"]
        assert meta["fetched_at"] == "2026-02-16T08:30:00Z"
        assert meta["cache_ttl_seconds"] == 60
        assert meta["details"] == {"count": 1}
        assert meta["served_from_cache"] is False
        assert meta["trace_id"] and meta["latency_ms"] >= 0

    @pytest.mark.asyncio
    async def test_repeat_call_is_served_from_cache(self, mcp_client, mock_client):
        """Test an identical second call does not reach the API."""
        mock_client.get.return_value = API_PAYLOAD

        first = await call(mcp_client, "get_weather_forecast", {"adm4_code": "31.74.04.1006"})
        second = await call(mcp_client, "get_weather_forecast", {"adm4_code": "31.74.04.1006"})

        assert mock_client.get.await_count == 1
        assert second["meta"]["served_from_cache"] is True
        assert second["data"] == first["data"]
        assert second["meta"]["trace_id"] != first["meta"]["trace_id"]

    @pytest.mark.asyncio
    async def test_different_arguments_are_cached_separately(self, mcp_client, mock_client):
        """Test another location is fetched, not answered from the first one's cache."""
        mock_client.get.return_value = API_PAYLOAD

        await call(mcp_client, "get_weather_forecast", {"adm4_code": "31.74.04.1006"})
        await call(mcp_client, "get_weather_forecast", {"adm4_code": "33.26.16.2005"})

        assert mock_client.get.await_count == 2


class TestErrorEnvelope:
    """Test failures are reported with stable codes and safe messages."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("failure,code", [
        (http_error(400), "INVALID_ARGUMENT"),
        (http_error(422), "INVALID_ARGUMENT"),
        (http_error(404), "NOT_FOUND"),
        (http_error(429), "RATE_LIMITED"),
        (http_error(502), "UPSTREAM_UNAVAILABLE"),
        (http_error(503), "UPSTREAM_UNAVAILABLE"),
        (httpx.ConnectTimeout("timed out"), "UPSTREAM_UNAVAILABLE"),
        (RuntimeError("secret-internal-detail"), "INTERNAL_ERROR"),
    ])
    async def test_failure_maps_to_code(self, mcp_client, mock_client, failure, code):
        """Test each kind of failure gets its code and leaks nothing internal."""
        mock_client.get.side_effect = failure

        envelope = await call(mcp_client, "get_latest_earthquake")

        assert envelope["status"] == "error"
        assert envelope["data"] is None
        assert envelope["error"]["code"] == code
        assert "secret-internal" not in str(envelope)
        assert envelope["meta"]["operation"] == "get_latest_earthquake"

    @pytest.mark.asyncio
    async def test_not_found_says_what_to_try(self, mcp_client, mock_client):
        """Test an unknown weather code points the caller to region search."""
        mock_client.get.side_effect = http_error(404)

        envelope = await call(mcp_client, "get_weather_forecast", {"adm4_code": "99.99.99.9999"})

        assert envelope["error"]["code"] == "NOT_FOUND"
        assert "search_regions" in envelope["error"]["message"]

    @pytest.mark.asyncio
    async def test_failures_are_not_cached(self, mcp_client, mock_client):
        """Test a call that failed is tried again next time."""
        mock_client.get.side_effect = [http_error(502), API_PAYLOAD]

        first = await call(mcp_client, "get_latest_earthquake")
        second = await call(mcp_client, "get_latest_earthquake")

        assert first["status"] == "error"
        assert second["status"] == "success"


class TestArgumentValidation:
    """Test malformed arguments are rejected before any request is made."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("tool,arguments", [
        ("get_weather_forecast", {"adm4_code": "1.2.3.4"}),
        ("get_current_weather", {"adm4_code": "31.74.04"}),
        ("get_nearby_earthquakes", {"latitude": 123.0, "longitude": 106.8}),
        ("get_nearby_earthquakes", {"latitude": -6.2, "longitude": 106.8, "radius_km": 5000}),
        ("get_districts", {"province_code": "311"}),
        ("get_subdistricts", {"district_code": "3174"}),
        ("get_villages", {"subdistrict_code": "31.74"}),
        ("search_regions", {"query": "a"}),
        ("search_regions", {"query": "tebet", "limit": 500}),
        ("get_weather_warnings", {"language": "fr"}),
        ("check_location_warnings", {"location": ""}),
    ])
    async def test_invalid_arguments_rejected(self, mcp_client, mock_client, tool, arguments):
        """Test the schema refuses the call and the API is never asked."""
        with pytest.raises(ToolError):
            await mcp_client.call_tool(tool, arguments)
        mock_client.get.assert_not_called()
