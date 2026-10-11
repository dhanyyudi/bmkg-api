"""Caching layer for MCP Server using existing app/cache infrastructure."""

import hashlib
import json
from typing import Any, Awaitable, Callable

# Import existing cache from app
try:
    from app.cache import cache
    HAS_CACHE = True
except ImportError:
    HAS_CACHE = False
    cache = None

# Cache TTLs (seconds)
CACHE_TTL = {
    "earthquake": 60,      # 1 minute
    "weather": 900,        # 15 minutes
    "nowcast": 120,        # 2 minutes
    "region": 86400,       # 24 hours (static data)
}


def generate_cache_key(tool_type: str, endpoint: str, params: dict[str, Any] | None) -> str:
    """Generate cache key for one API request."""
    key_data = json.dumps([endpoint, params or {}], sort_keys=True, default=str)
    return f"mcp:{tool_type}:{hashlib.md5(key_data.encode()).hexdigest()}"


async def get_or_fetch(
    tool_type: str,
    endpoint: str,
    params: dict[str, Any] | None,
    fetch: Callable[[], Awaitable[dict]],
) -> tuple[dict, bool]:
    """Return an API payload from cache, or fetch and cache it.

    Only successful payloads are stored: a failed fetch raises and is retried
    on the next call. Cache trouble never fails the call.

    Returns:
        Tuple of (payload, from_cache)
    """
    if not HAS_CACHE or cache is None:
        return await fetch(), False

    cache_key = generate_cache_key(tool_type, endpoint, params)
    try:
        cached_data = await cache.get(cache_key)
        if cached_data:
            return cached_data, True
    except Exception:
        pass

    payload = await fetch()

    try:
        await cache.set(cache_key, payload, ttl=CACHE_TTL.get(tool_type, 300))
    except Exception:
        pass

    return payload, False
