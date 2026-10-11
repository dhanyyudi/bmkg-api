"""Cache-Control headers so a CDN in front of the API can absorb repeat requests."""

from app.config import settings

# Client errors are cached briefly so a repeated bad request does not reach BMKG every time.
CLIENT_ERROR_TTL = 60

UNCACHED_PATHS = ("/health", "/ready")


def endpoint_ttl(path: str) -> int | None:
    """Return the cache TTL configured for an API path, or None if the path has none."""
    if path == "/v1/earthquake/latest":
        return settings.cache_ttl_earthquake_latest
    if path.startswith("/v1/earthquake/"):
        return settings.cache_ttl_earthquake_list
    if path.startswith("/v1/nowcast"):
        return settings.cache_ttl_nowcast
    if path.startswith("/v1/weather/"):
        return settings.cache_ttl_weather
    if path.startswith("/v1/wilayah/"):
        return settings.cache_ttl_wilayah
    return None


def website_cache_control(path: str, status_code: int) -> str | None:
    """Cache policy for the website's own files.

    Build output under /_app/immutable/ has a content hash in its name and never
    changes. Pages must be revalidated: a page cached across a deploy would ask
    for script files that no longer exist.
    """
    if status_code != 200:
        return None
    if path.startswith("/_app/immutable/"):
        return "public, max-age=31536000, immutable"
    last = path.rsplit("/", 1)[-1]
    if last == "" or last.endswith(".html"):
        return "no-cache"
    return None


def cache_control_for(path: str, status_code: int, remaining_ttl: str | None = None) -> str | None:
    """Build the Cache-Control value for a response.

    Args:
        path: Request path
        status_code: Response status code
        remaining_ttl: Seconds left on the server-side cache entry (X-Cache-TTL), if known

    Returns:
        Cache-Control value, or None to leave the response untouched
    """
    if path in UNCACHED_PATHS:
        return "no-store"

    ttl = endpoint_ttl(path)
    if ttl is None:
        return website_cache_control(path, status_code)

    if status_code == 200:
        # Expire together with the server-side cache entry, so the CDN never
        # stretches staleness beyond the configured TTL.
        if remaining_ttl is not None and remaining_ttl.isdigit():
            ttl = min(ttl, int(remaining_ttl))
        return f"public, max-age={ttl}"

    if 400 <= status_code < 500 and status_code != 429:
        return f"public, max-age={min(ttl, CLIENT_ERROR_TTL)}"

    # Rate-limit and upstream errors must never be served to other clients.
    return "no-store"
