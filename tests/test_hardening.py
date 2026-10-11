"""Tests for abuse protections: upstream budget, single flight, input bounds."""

import asyncio

import httpx
import pytest
from fastapi.testclient import TestClient
from unittest.mock import AsyncMock, patch

from app.cache import InMemoryCache, cache, single_flight
from app.dependencies import _rate_limit_key
from app.http_client import RequestBudget, UpstreamBudgetExceeded
from app.main import app
from app.models.nowcast import ActiveProvince
from app.services.nowcast_service import nowcast_service
from app.services.weather_service import weather_service


@pytest.fixture(autouse=True)
def fresh_cache():
    """Give each test an empty in-memory cache."""
    with patch.object(cache, "_use_fallback", True), \
            patch.object(cache, "_fallback", InMemoryCache()):
        yield


def not_found_error() -> httpx.HTTPStatusError:
    """Build the error httpx raises for an upstream 404."""
    request = httpx.Request("GET", "https://api.bmkg.go.id/publik/prakiraan-cuaca")
    return httpx.HTTPStatusError("404 Not Found", request=request, response=httpx.Response(404, request=request))


class TestRequestBudget:
    """Test the cap on requests sent to BMKG."""

    def test_allows_up_to_limit_then_refuses(self):
        """Test requests beyond the per-minute budget are refused."""
        budget = RequestBudget(per_minute=3)
        for _ in range(3):
            budget.acquire()
        with pytest.raises(UpstreamBudgetExceeded):
            budget.acquire()

    def test_budget_refills_after_a_minute(self, monkeypatch):
        """Test old requests stop counting once they are a minute old."""
        now = [1000.0]
        monkeypatch.setattr("app.http_client.time.monotonic", lambda: now[0])
        budget = RequestBudget(per_minute=1)
        budget.acquire()
        now[0] += 61
        budget.acquire()

    def test_zero_disables_the_cap(self):
        """Test a budget of 0 never refuses."""
        budget = RequestBudget(per_minute=0)
        for _ in range(500):
            budget.acquire()


class TestSingleFlight:
    """Test that concurrent cache misses share one upstream call."""

    @pytest.mark.asyncio
    async def test_concurrent_misses_fetch_once(self, sample_forecast):
        """Test ten simultaneous requests for one location call BMKG once."""
        calls = 0

        async def slow_fetch(adm4_code):
            nonlocal calls
            calls += 1
            await asyncio.sleep(0.05)
            return sample_forecast

        with patch.object(weather_service, "_fetch_from_bmkg", side_effect=slow_fetch):
            results = await asyncio.gather(
                *[weather_service.get_forecast("33.26.16.1001") for _ in range(10)]
            )

        assert calls == 1
        assert len(results) == 10

    @pytest.mark.asyncio
    async def test_lock_is_released_after_failure(self):
        """Test a failed refresh does not block the next caller."""
        with pytest.raises(RuntimeError):
            async with single_flight("k"):
                raise RuntimeError("boom")
        async with single_flight("k"):
            pass


class TestWeatherCodeValidation:
    """Test that only canonical ADM4 codes reach BMKG."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("code", [
        "1.2.3.4", "033.26.16.1001", "33.26.16.10010", "33.26.16", "-3.26.16.1001",
        "33.26.16.1001 ", "33,26,16,1001", "aa.bb.cc.dddd",
    ])
    async def test_malformed_codes_are_rejected_without_fetching(self, code):
        """Test malformed codes fail validation and never call BMKG."""
        with patch.object(weather_service, "_fetch_from_bmkg", new=AsyncMock()) as fetch:
            with pytest.raises(ValueError):
                await weather_service.get_forecast(code)
        fetch.assert_not_called()

    @pytest.mark.asyncio
    async def test_unknown_code_is_remembered(self):
        """Test a code BMKG does not know is only asked for once."""
        fetch = AsyncMock(side_effect=not_found_error())
        with patch.object(weather_service, "_fetch_from_bmkg", new=fetch):
            for _ in range(3):
                with pytest.raises(Exception, match="404"):
                    await weather_service.get_forecast("99.99.99.9999")
        assert fetch.call_count == 1


class TestNowcastDetail:
    """Test that only active alert codes reach BMKG."""

    @pytest.mark.asyncio
    async def test_inactive_code_is_not_fetched(self):
        """Test a code missing from the active feed returns nothing without a CAP fetch."""
        active = [ActiveProvince(code="CBT20260216004", province="Banten", description="x", published_at="2026-02-16T07:00:00Z", detail_url="/v1/nowcast/CBT20260216004")]
        with patch.object(nowcast_service, "_get_cached_or_fetch_rss", new=AsyncMock(return_value=(active, True))), \
                patch.object(nowcast_service, "_fetch_cap_xml", new=AsyncMock()) as fetch_cap:
            warning, _, _, _ = await nowcast_service.get_warning_detail("MADEUP123", "id")
        assert warning is None
        fetch_cap.assert_not_called()

    def test_malformed_alert_code_is_rejected(self):
        """Test alert codes with unexpected characters fail validation."""
        response = TestClient(app).get("/v1/nowcast/bad code!")
        assert response.status_code == 422


class TestLocationCheck:
    """Test the location check endpoint."""

    def test_check_route_is_not_shadowed_by_alert_code(self):
        """Test /check reaches the location check, not the alert detail route."""
        active = [ActiveProvince(code="CBT20260216004", province="Banten", description="x", published_at="2026-02-16T07:00:00Z", detail_url="/v1/nowcast/CBT20260216004")]
        with patch.object(nowcast_service, "_get_cached_or_fetch_rss", new=AsyncMock(return_value=(active, True))), \
                patch.object(nowcast_service, "_get_cached_or_fetch_cap", new=AsyncMock(return_value=(None, True))):
            response = TestClient(app).get("/v1/nowcast/check", params={"location": "Serang"})
        assert response.status_code == 200
        assert response.json()["data"]["location"] == "Serang"

    @pytest.mark.asyncio
    async def test_spent_budget_is_not_reported_as_no_warnings(self):
        """Test the scan fails loudly when BMKG could not be asked."""
        active = [ActiveProvince(code="CBT20260216004", province="Banten", description="x", published_at="2026-02-16T07:00:00Z", detail_url="/v1/nowcast/CBT20260216004")]
        with patch.object(nowcast_service, "_get_cached_or_fetch_rss", new=AsyncMock(return_value=(active, True))), \
                patch.object(nowcast_service, "_get_cached_or_fetch_cap", new=AsyncMock(side_effect=UpstreamBudgetExceeded("spent"))):
            with pytest.raises(UpstreamBudgetExceeded):
                await nowcast_service.check_location("Serang", "id")


class TestInputBounds:
    """Test length limits on free-text parameters."""

    def test_search_query_too_long(self):
        """Test an oversized search query is rejected."""
        response = TestClient(app).get("/v1/wilayah/search", params={"q": "a" * 101})
        assert response.status_code == 422

    def test_location_too_long(self):
        """Test an oversized location name is rejected."""
        response = TestClient(app).get("/v1/nowcast/check", params={"location": "a" * 101})
        assert response.status_code == 422


class TestRateLimitKey:
    """Test how client addresses map to rate limit buckets."""

    def test_ipv4_is_kept(self):
        """Test an IPv4 address is its own bucket."""
        assert _rate_limit_key("203.0.113.7") == "203.0.113.7"

    def test_ipv6_addresses_in_one_prefix_share_a_bucket(self):
        """Test two addresses in the same /64 count as one client."""
        a = _rate_limit_key("2001:db8:1:2:aaaa:bbbb:cccc:dddd")
        b = _rate_limit_key("2001:db8:1:2::1")
        assert a == b == "2001:db8:1:2::/64"

    def test_ipv6_other_prefix_is_separate(self):
        """Test a different /64 gets a different bucket."""
        assert _rate_limit_key("2001:db8:1:3::1") != _rate_limit_key("2001:db8:1:2::1")

    def test_unparseable_value_is_kept(self):
        """Test a value that is not an IP address is used as is."""
        assert _rate_limit_key("unknown") == "unknown"
