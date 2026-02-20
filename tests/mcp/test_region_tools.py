"""Tests for region tools."""

import pytest
from mcp_server.tools.region import (
    search_regions,
    get_provinces,
    get_districts,
    get_subdistricts,
    get_villages,
)


@pytest.mark.asyncio
async def test_search_regions(mock_client):
    """Test searching for regions."""
    mock_response = {
        "data": [
            {"code": "31.74.01", "name": "Tebet", "type": "kecamatan"},
            {"code": "31.74", "name": "Jakarta Selatan", "type": "kota"},
        ]
    }
    mock_client.get.return_value = mock_response

    result = await search_regions("tebet")

    assert result == mock_response
    mock_client.get.assert_called_with("/wilayah/search", params={"q": "tebet"})


@pytest.mark.asyncio
async def test_search_regions_multiple_words(mock_client):
    """Test searching with multiple words."""
    mock_response = {"data": []}
    mock_client.get.return_value = mock_response

    result = await search_regions("jakarta selatan")

    assert result == mock_response
    mock_client.get.assert_called_with("/wilayah/search", params={"q": "jakarta selatan"})


@pytest.mark.asyncio
async def test_get_provinces(mock_client):
    """Test getting all provinces."""
    mock_response = {
        "data": [
            {"code": "31", "name": "DKI Jakarta"},
            {"code": "32", "name": "Jawa Barat"},
        ]
    }
    mock_client.get.return_value = mock_response

    result = await get_provinces()

    assert result == mock_response
    mock_client.get.assert_called_once_with("/wilayah/provinces")


@pytest.mark.asyncio
async def test_get_districts(mock_client):
    """Test getting districts for a province."""
    mock_response = {
        "data": [
            {"code": "31.71", "name": "Jakarta Pusat"},
            {"code": "31.74", "name": "Jakarta Selatan"},
        ]
    }
    mock_client.get.return_value = mock_response

    result = await get_districts("31")

    assert result == mock_response
    mock_client.get.assert_called_with("/wilayah/districts", params={"province": "31"})


@pytest.mark.asyncio
async def test_get_subdistricts(mock_client):
    """Test getting subdistricts for a district."""
    mock_response = {
        "data": [
            {"code": "31.74.01", "name": "Tebet"},
            {"code": "31.74.04", "name": "Pasar Minggu"},
        ]
    }
    mock_client.get.return_value = mock_response

    result = await get_subdistricts("31.74")

    assert result == mock_response
    mock_client.get.assert_called_with("/wilayah/subdistricts", params={"district": "31.74"})


@pytest.mark.asyncio
async def test_get_villages(mock_client):
    """Test getting villages for a subdistrict."""
    mock_response = {
        "data": [
            {"code": "31.74.04.1006", "name": "Pejaten Barat"},
            {"code": "31.74.04.1007", "name": "Pejaten Timur"},
        ]
    }
    mock_client.get.return_value = mock_response

    result = await get_villages("31.74.04")

    assert result == mock_response
    mock_client.get.assert_called_with("/wilayah/villages", params={"subdistrict": "31.74.04"})


@pytest.mark.asyncio
async def test_get_districts_different_province(mock_client):
    """Test getting districts for different province code."""
    mock_response = {"data": [{"code": "32.01", "name": "Kabupaten Bogor"}]}
    mock_client.get.return_value = mock_response

    result = await get_districts("32")

    assert result == mock_response
    mock_client.get.assert_called_with("/wilayah/districts", params={"province": "32"})


@pytest.mark.asyncio
async def test_search_regions_error(mock_client):
    """Test error handling in search_regions."""
    mock_client.get.side_effect = Exception("Network error")

    result = await search_regions("test")

    assert "error" in result
    assert "Terjadi kesalahan" in result["error"]


@pytest.mark.asyncio
async def test_get_villages_error(mock_client):
    """Test error handling in get_villages."""
    from httpx import HTTPStatusError

    mock_response = AsyncMock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"

    error = HTTPStatusError("Not Found", request=AsyncMock(), response=mock_response)
    mock_client.get.side_effect = error

    result = await get_villages("99.99.99")

    assert "error" in result
