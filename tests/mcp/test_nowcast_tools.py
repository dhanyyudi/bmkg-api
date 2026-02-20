"""Tests for nowcast (weather warnings) tools."""

import pytest
from mcp_server.tools.nowcast import get_weather_warnings, check_location_warnings


@pytest.mark.asyncio
async def test_get_weather_warnings(mock_client):
    """Test getting active weather warnings."""
    mock_response = {
        "data": [
            {
                "province": "DKI Jakarta",
                "alert_code": "DKI_JAKARTA_001",
                "warning_type": "Heavy Rain",
                "severity": "Moderate",
            },
            {
                "province": "Jawa Barat",
                "alert_code": "JAWA_BARAT_002",
                "warning_type": "Strong Wind",
                "severity": "High",
            },
        ]
    }
    mock_client.get.return_value = mock_response

    result = await get_weather_warnings()

    assert result == mock_response
    mock_client.get.assert_called_once_with("/nowcast")


@pytest.mark.asyncio
async def test_get_weather_warnings_empty(mock_client):
    """Test getting weather warnings when none active."""
    mock_response = {"data": []}
    mock_client.get.return_value = mock_response

    result = await get_weather_warnings()

    assert result == mock_response
    assert result["data"] == []


@pytest.mark.asyncio
async def test_check_location_warnings(mock_client):
    """Test checking warnings for a specific location."""
    mock_response = {
        "data": {
            "location": "Jakarta",
            "has_warning": True,
            "warnings": [
                {"type": "Heavy Rain", "severity": "Moderate"}
            ],
        }
    }
    mock_client.get.return_value = mock_response

    result = await check_location_warnings("Jakarta")

    assert result == mock_response
    mock_client.get.assert_called_with("/nowcast/check", params={"location": "Jakarta"})


@pytest.mark.asyncio
async def test_check_location_warnings_no_warnings(mock_client):
    """Test checking warnings when location has no active warnings."""
    mock_response = {
        "data": {
            "location": "Surabaya",
            "has_warning": False,
            "warnings": [],
        }
    }
    mock_client.get.return_value = mock_response

    result = await check_location_warnings("Surabaya")

    assert result == mock_response
    assert result["data"]["has_warning"] is False


@pytest.mark.asyncio
async def test_check_location_warnings_different_locations(mock_client):
    """Test checking warnings for different locations."""
    locations = ["Bandung", "Yogyakarta", "Medan", "Makassar"]

    for location in locations:
        mock_response = {"data": {"location": location, "has_warning": False}}
        mock_client.get.return_value = mock_response

        result = await check_location_warnings(location)

        assert result["data"]["location"] == location
        mock_client.get.assert_called_with("/nowcast/check", params={"location": location})


@pytest.mark.asyncio
async def test_get_weather_warnings_error(mock_client):
    """Test error handling in get_weather_warnings."""
    mock_client.get.side_effect = Exception("Connection timeout")

    result = await get_weather_warnings()

    assert "error" in result
    assert "Terjadi kesalahan" in result["error"]


@pytest.mark.asyncio
async def test_check_location_warnings_error(mock_client):
    """Test error handling in check_location_warnings."""
    from httpx import HTTPStatusError

    mock_response = AsyncMock()
    mock_response.status_code = 502
    mock_response.text = "Bad Gateway"

    error = HTTPStatusError("Bad Gateway", request=AsyncMock(), response=mock_response)
    mock_client.get.side_effect = error

    result = await check_location_warnings("Jakarta")

    assert "error" in result
    assert "BMKG" in result["error"] or "tidak tersedia" in result["error"]


@pytest.mark.asyncio
async def test_check_location_warnings_special_characters(mock_client):
    """Test checking warnings with location containing special characters."""
    mock_response = {"data": {"location": "D.I. Yogyakarta", "has_warning": False}}
    mock_client.get.return_value = mock_response

    result = await check_location_warnings("D.I. Yogyakarta")

    assert result == mock_response
    mock_client.get.assert_called_with("/nowcast/check", params={"location": "D.I. Yogyakarta"})
