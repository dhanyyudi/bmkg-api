"""Dependencies for FastAPI routes.

This module provides rate limiting without API key authentication.
Since this API is designed for self-hosting, we use simple anonymous
rate limiting only.
"""

from fastapi import Request
from slowapi import Limiter
from slowapi.util import get_remote_address
from app.config import settings


# Initialize rate limiter with IP-based keying
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[settings.rate_limit_anonymous],
    headers_enabled=True,
)


# Note: API key authentication has been removed.
# This API is designed for self-hosting where users control their own
# rate limits. The demo instance uses simple IP-based rate limiting.
# For production use, please self-host: https://github.com/dhanypedia/bmkg-api
