"""Tests for earthquake tools."""

import pytest
from mcp_server.tools.earthquake import (
    get_latest_earthquake,
    get_recent_earthquakes,
    get_felt_earthquakes,
    get_nearby_earthquakes,
)


@pytest.mark.asyncio
async def test_get_latest_earthquake(mock_client):
    """Test getting the latest earthquake data."""
    mock_response = {
        "data": {
            "magnitude": "5.5",
            "location": "Test Location",
            "depth": "10 km",
            "coordinates": {"lat": -6.0, "lon": 106.0},
        }
    }
    mock_client.get.return_value = mock_response

    result = await get_latest_earthquake()

    assert result == mock_response
    mock_client.get.assert_called_once_with("/earthquake/latest")


@pytest.mark.asyncio
async def test_get_recent_earthquakes(mock_client):
    """Test getting recent earthquakes with magnitude 5.0+."""
    mock_response = {
        "data": [
            {"magnitude": "5.5", "location": "Location 1"},
            {"magnitude": "6.0", "location": "Location 2"},
        ]
    }
    mock_client.get.return_value = mock_response

    result = await get_recent_earthquakes()

    assert result == mock_response
    mock_client.get.assert_called_once_with("/earthquake/recent")


@pytest.mark.asyncio
async def test_get_felt_earthquakes(mock_client):
    """Test getting earthquakes that were felt by people."""
    mock_response = {
        "data": [
            {"magnitude": "4.5", "location": "Felt Location", "felt": "Dirasakan"}
        ]
    }
    mock_client.get.return_value = mock_response

    result = await get_felt_earthquakes()

    assert result == mock_response
    mock_client.get.assert_called_once_with("/earthquake/felt")


@pytest.mark.asyncio
async def test_get_nearby_earthquakes(mock_client):
    """Test finding earthquakes near specific coordinates."""
    mock_response = {"data": [{"magnitude": "4.0", "distance": "50 km"}]}
    mock_client.get.return_value = mock_response

    result = await get_nearby_earthquakes(-6.2088, 106.8456, 100)

    assert result == mock_response
    mock_client.get.assert_called_with(
        "/earthquake/nearby",
        params={"lat": -6.2088, "lon": 106.8456, "radius_km": 100},
    )


@pytest.mark.asyncio
async def test_get_nearby_earthquakes_invalid_coords(mock_client):
    """Test nearby earthquakes with invalid coordinates returns error."""
    result = await get_nearby_earthquakes(999, 999, 100)

    assert "error" in result
    assert "Koordinat tidak valid" in result["error"]
    mock_client.get.assert_not_called()


@pytest.mark.asyncio
async def test_get_nearby_earthquakes_default_radius(mock_client):
    """Test nearby earthquakes with default radius."""
    mock_response = {"data": []}
    mock_client.get.return_value = mock_response

    result = await get_nearby_earthquakes(-6.2088, 106.8456)

    assert result == mock_response
    mock_client.get.assert_called_with(
        "/earthquake/nearby",
        params={"lat": -6.2088, "lon": 106.8456, "radius_km": 100},
    )


@pytest.mark.asyncio
async def test_get_nearby_earthquakes_radius_clamping(mock_client):
    """Test that radius is clamped to max 500km."""
    mock_response = {"data": []}
    mock_client.get.return_value = mock_response

    # Test with radius > 500
    await get_nearby_earthquakes(-6.2088, 106.8456, 1000)

    mock_client.get.assert_called_with(
        "/earthquake/nearby",
        params={"lat": -6.2088, "lon": 106.8456, "radius_km": 500},
    )


@pytest.mark.asyncio
async def test_get_nearby_earthquakes_radius_min_clamping(mock_client):
    """Test that radius is clamped to min 1km."""
    mock_response = {"data": []}
    mock_client.get.return_value = mock_response

    # Test with radius < 1
    await get_nearby_earthquakes(-6.2088, 106.8456, 0)

    mock_client.get.assert_called_with(
        "/earthquake/nearby",
        params={"lat": -6.2088, "lon": 106.8456, "radius_km": 1},
    )


@pytest.mark.asyncio
async def test_get_latest_earthquake_error(mock_client):
    """Test error handling in get_latest_earthquake."""
    from httpx import HTTPStatusError

    # Create a mock response with 404 status
    mock_response = AsyncMock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"

    error = HTTPStatusError("Not Found", request=AsyncMock(), response=mock_response)
    mock_client.get.side_effect = error

    result = await get_latest_earthquake()

    assert "error" in result
    assert "tidak ditemukan" in result["error"]
