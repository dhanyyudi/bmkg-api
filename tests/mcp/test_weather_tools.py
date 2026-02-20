"""Tests for weather tools."""

import pytest
from mcp_server.tools.weather import get_weather_forecast, get_current_weather


@pytest.mark.asyncio
async def test_get_weather_forecast(mock_client):
    """Test getting weather forecast for a location."""
    mock_response = {
        "data": {
            "lokasi": {"deskel": "Pejaten Barat", "kabkota": "Jakarta Selatan"},
            "cuaca": [[{"temperature": 30, "weather": "Cerah"}]],
        }
    }
    mock_client.get.return_value = mock_response

    result = await get_weather_forecast("31.74.04.1006")

    assert result == mock_response
    mock_client.get.assert_called_with("/weather/31.74.04.1006")


@pytest.mark.asyncio
async def test_get_current_weather(mock_client):
    """Test getting current weather for a location."""
    mock_response = {
        "data": {"current": {"temperature": 28, "humidity": 75, "weather": "Berawan"}}
    }
    mock_client.get.return_value = mock_response

    result = await get_current_weather("31.74.04.1006")

    assert result == mock_response
    mock_client.get.assert_called_with("/weather/31.74.04.1006/current")


@pytest.mark.asyncio
async def test_get_weather_forecast_different_code(mock_client):
    """Test weather forecast with different adm4 code."""
    mock_response = {"data": {"lokasi": {"deskel": "Tebet"}, "cuaca": []}}
    mock_client.get.return_value = mock_response

    result = await get_weather_forecast("31.74.01.1001")

    assert result == mock_response
    mock_client.get.assert_called_with("/weather/31.74.01.1001")


@pytest.mark.asyncio
async def test_get_weather_forecast_error(mock_client):
    """Test error handling when API returns error."""
    from httpx import HTTPStatusError

    mock_response = AsyncMock()
    mock_response.status_code = 502
    mock_response.text = "Bad Gateway"

    error = HTTPStatusError("Bad Gateway", request=AsyncMock(), response=mock_response)
    mock_client.get.side_effect = error

    result = await get_weather_forecast("31.74.04.1006")

    assert "error" in result
    assert "BMKG" in result["error"] or "salah" in result["error"].lower()


@pytest.mark.asyncio
async def test_get_current_weather_404_error(mock_client):
    """Test error handling for 404 (location not found)."""
    from httpx import HTTPStatusError

    mock_response = AsyncMock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"

    error = HTTPStatusError("Not Found", request=AsyncMock(), response=mock_response)
    mock_client.get.side_effect = error

    result = await get_current_weather("99.99.99.9999")

    assert "error" in result
    assert "tidak ditemukan" in result["error"] or "wilayah" in result["error"]
