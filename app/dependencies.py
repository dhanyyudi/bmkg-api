"""Dependencies for FastAPI routes.

This module provides rate limiting without API key authentication.
Since this API is designed for self-hosting, we use simple anonymous
rate limiting only.
"""

import ipaddress

from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.config import settings


def get_client_ip(request: Request) -> str:
    """Return the client IP used as the rate limit key.

    Behind a proxy the socket address is the proxy's, which would put every
    client in one bucket, so read the configured header first.
    """
    if settings.client_ip_header:
        forwarded = request.headers.get(settings.client_ip_header)
        if forwarded:
            return _rate_limit_key(forwarded.split(",")[0].strip())
    return _rate_limit_key(get_remote_address(request))


def _rate_limit_key(ip: str) -> str:
    """Count an IPv6 /64 as one client: a single user controls the whole prefix."""
    try:
        if ipaddress.ip_address(ip).version == 6:
            return str(ipaddress.ip_network(f"{ip}/64", strict=False))
    except ValueError:
        pass
    return ip


# Initialize rate limiter with IP-based keying
limiter = Limiter(
    key_func=get_client_ip,
    default_limits=[settings.rate_limit_anonymous],
    headers_enabled=True,
)


# Note: API key authentication has been removed.
# This API is designed for self-hosting where users control their own
# rate limits. The demo instance uses simple IP-based rate limiting.
# For production use, please self-host: https://github.com/dhanypedia/bmkg-api
