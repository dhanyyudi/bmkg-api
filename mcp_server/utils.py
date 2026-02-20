import httpx


def format_error_message(error: Exception) -> str:
    """Format error into user-friendly message."""
    if isinstance(error, httpx.HTTPStatusError):
        if error.response.status_code == 404:
            return "Data tidak ditemukan. Pastikan kode wilayah valid."
        elif error.response.status_code == 502:
            return "Server BMKG sedang tidak tersedia. Silakan coba lagi nanti."
    return f"Terjadi kesalahan: {str(error)}"


def validate_coordinates(lat: float, lon: float) -> bool:
    """Validate latitude and longitude."""
    return -90 <= lat <= 90 and -180 <= lon <= 180


def validate_radius(radius_km: int) -> int:
    """Validate and clamp radius to max 500km."""
    return min(max(radius_km, 1), 500)
