"""Tests for utility functions."""

import pytest
import httpx
from unittest.mock import AsyncMock

from mcp_server.utils import (
    format_error_message,
    validate_coordinates,
    validate_radius,
)


class TestFormatErrorMessage:
    """Tests for format_error_message function."""

    def test_404_error(self):
        """Test formatting 404 error."""
        mock_response = AsyncMock()
        mock_response.status_code = 404

        error = httpx.HTTPStatusError(
            "Not Found",
            request=AsyncMock(),
            response=mock_response
        )

        result = format_error_message(error)

        assert "tidak ditemukan" in result
        assert "wilayah" in result

    def test_502_error(self):
        """Test formatting 502 error."""
        mock_response = AsyncMock()
        mock_response.status_code = 502

        error = httpx.HTTPStatusError(
            "Bad Gateway",
            request=AsyncMock(),
            response=mock_response
        )

        result = format_error_message(error)

        assert "BMKG" in result
        assert "tidak tersedia" in result

    def test_other_http_error(self):
        """Test formatting other HTTP errors."""
        mock_response = AsyncMock()
        mock_response.status_code = 500

        error = httpx.HTTPStatusError(
            "Internal Server Error",
            request=AsyncMock(),
            response=mock_response
        )

        result = format_error_message(error)

        assert "Terjadi kesalahan" in result
        assert "Internal Server Error" in result

    def test_generic_exception(self):
        """Test formatting generic exception."""
        error = ValueError("Invalid input")

        result = format_error_message(error)

        assert "Terjadi kesalahan" in result
        assert "Invalid input" in result


class TestValidateCoordinates:
    """Tests for validate_coordinates function."""

    def test_valid_coordinates_jakarta(self):
        """Test valid coordinates for Jakarta."""
        assert validate_coordinates(-6.2088, 106.8456) is True

    def test_valid_coordinates_bali(self):
        """Test valid coordinates for Bali."""
        assert validate_coordinates(-8.4095, 115.1889) is True

    def test_valid_coordinates_north_pole(self):
        """Test valid coordinates at North Pole."""
        assert validate_coordinates(90, 0) is True

    def test_valid_coordinates_south_pole(self):
        """Test valid coordinates at South Pole."""
        assert validate_coordinates(-90, 0) is True

    def test_valid_coordinates_dateline(self):
        """Test valid coordinates at international dateline."""
        assert validate_coordinates(0, 180) is True
        assert validate_coordinates(0, -180) is True

    def test_invalid_latitude_too_high(self):
        """Test invalid latitude above 90."""
        assert validate_coordinates(91, 106.8456) is False

    def test_invalid_latitude_too_low(self):
        """Test invalid latitude below -90."""
        assert validate_coordinates(-91, 106.8456) is False

    def test_invalid_longitude_too_high(self):
        """Test invalid longitude above 180."""
        assert validate_coordinates(-6.2088, 181) is False

    def test_invalid_longitude_too_low(self):
        """Test invalid longitude below -180."""
        assert validate_coordinates(-6.2088, -181) is False

    def test_invalid_coordinates_both(self):
        """Test invalid coordinates for both lat and lon."""
        assert validate_coordinates(999, 999) is False

    def test_edge_cases_exact_limits(self):
        """Test exact boundary values."""
        assert validate_coordinates(90, 180) is True
        assert validate_coordinates(-90, -180) is True


class TestValidateRadius:
    """Tests for validate_radius function."""

    def test_valid_radius_default(self):
        """Test valid default radius."""
        assert validate_radius(100) == 100

    def test_valid_radius_middle(self):
        """Test valid middle radius."""
        assert validate_radius(250) == 250

    def test_valid_radius_max(self):
        """Test valid maximum radius."""
        assert validate_radius(500) == 500

    def test_valid_radius_min(self):
        """Test valid minimum radius."""
        assert validate_radius(1) == 1

    def test_radius_clamped_to_max(self):
        """Test radius clamped to max 500."""
        assert validate_radius(501) == 500
        assert validate_radius(1000) == 500
        assert validate_radius(9999) == 500

    def test_radius_clamped_to_min(self):
        """Test radius clamped to min 1."""
        assert validate_radius(0) == 1
        assert validate_radius(-1) == 1
        assert validate_radius(-100) == 1

    def test_radius_zero(self):
        """Test radius of zero is clamped to 1."""
        assert validate_radius(0) == 1
