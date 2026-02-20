"""Caching layer for MCP Server using existing app/cache infrastructure."""

import json
import hashlib
from typing import Optional, Any
from functools import wraps

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


def generate_cache_key(prefix: str, *args, **kwargs) -> str:
    """Generate cache key from function arguments."""
    key_data = f"{prefix}:{args}:{kwargs}"
    return hashlib.md5(key_data.encode()).hexdigest()


def cached(tool_type: str):
    """Decorator to cache MCP tool responses."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not HAS_CACHE or cache is None:
                return await func(*args, **kwargs)
            
            # Generate cache key
            cache_key = generate_cache_key(
                f"mcp:{tool_type}:{func.__name__}",
                *args,
                **kwargs
            )
            
            # Try to get from cache
            try:
                cached_data = await cache.get(cache_key)
                if cached_data:
                    return cached_data
            except Exception:
                pass  # Cache miss or error, continue to fetch
            
            # Call the function
            result = await func(*args, **kwargs)
            
            # Store in cache (only if no error)
            if "error" not in result:
                try:
                    ttl = CACHE_TTL.get(tool_type, 300)
                    await cache.set(cache_key, result, ttl=ttl)
                except Exception:
                    pass  # Cache set error, ignore
            
            return result
        return wrapper
    return decorator


def invalidate_cache(pattern: str = "mcp:*"):
    """Invalidate cache by pattern (if supported by cache backend)."""
    if HAS_CACHE and cache and hasattr(cache, 'delete_pattern'):
        try:
            cache.delete_pattern(pattern)
        except Exception:
            pass
