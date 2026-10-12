"""Main FastAPI application."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app import __version__
from app.config import settings
from app.cache import cache
from app.cache_headers import cache_control_for
from app.dependencies import limiter
from app.http_client import close_http_client
from app.routers import earthquake, health, nowcast, weather, wilayah

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level.upper()),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    logger.info("Starting up BMKG API...")
    await cache.connect()
    if cache.is_using_fallback():
        logger.info("Using in-memory cache (Redis unavailable)")
    else:
        logger.info("Connected to Redis")
    yield
    # Shutdown
    logger.info("Shutting down BMKG API...")
    await cache.disconnect()
    await close_http_client()
    logger.info("Cleanup complete")


# OpenAPI tags metadata
TAGS_METADATA = [
    {
        "name": "earthquake",
        "description": "Earthquake data from BMKG seismic network",
        "externalDocs": {
            "description": "BMKG Earthquake Data",
            "url": "https://data.bmkg.go.id/gempabumi/",
        },
    },
    {
        "name": "weather",
        "description": "Weather forecasts for Indonesian regions",
        "externalDocs": {
            "description": "BMKG Weather Data",
            "url": "https://data.bmkg.go.id/prakiraan-cuaca/",
        },
    },
    {
        "name": "nowcast",
        "description": "Weather warnings and early alerts (Peringatan Dini)",
        "externalDocs": {
            "description": "BMKG Nowcast Information",
            "url": "https://data.bmkg.go.id/peringatan-dini-cuaca/",
        },
    },
    {
        "name": "wilayah",
        "description": "Region lookup service for Indonesian administrative areas",
    },
    {
        "name": "health",
        "description": "Health and readiness checks",
    },
]

# Simple description without markdown tables
DESCRIPTION = """
REST API for Indonesian Weather & Earthquake Data from BMKG.

**Features:**
- Earthquake Data: Latest, recent (M 5.0+), felt earthquakes, nearby search
- Weather Forecasts: 3-day forecasts for any kelurahan/desa in Indonesia  
- Weather Warnings: Real-time severe weather alerts (Nowcast)
- Region Lookup: Navigate Indonesian administrative regions

**Rate Limits:**
- Anonymous: 30 requests/minute
- No API key required

**Attribution:**
All data belongs to BMKG (Badan Meteorologi, Klimatologi, dan Geofisika).
This API is not affiliated with BMKG.

**Source Code:** https://github.com/dhanypedia/bmkg-api
"""

# Create FastAPI app with clean metadata
app = FastAPI(
    title="BMKG API",
    description=DESCRIPTION,
    version=__version__,
    docs_url=None,  # Disable default Swagger UI
    redoc_url="/redoc",  # /docs is the website's own documentation page
    openapi_url="/openapi.json",
    lifespan=lifespan,
    openapi_tags=TAGS_METADATA,
    contact={
        "name": "Dhany",
        "url": "https://github.com/dhanyyudi/bmkg-api",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
    servers=[
        {"url": "https://bmkg-api.dhanypedia.com", "description": "Public demo"},
        {"url": "http://localhost:8099", "description": "Local development"},
    ],
)

# Add rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)


@app.middleware("http")
async def add_cache_control(request: Request, call_next):
    """Mark API responses as cacheable so a CDN can serve repeat requests."""
    response = await call_next(request)
    if request.method == "GET" and "cache-control" not in response.headers:
        cache_control = cache_control_for(
            request.url.path,
            response.status_code,
            response.headers.get("X-Cache-TTL"),
        )
        if cache_control:
            response.headers["Cache-Control"] = cache_control
            if request.url.path.startswith("/v1/"):
                # CORSMiddleware only answers requests that send Origin. A CDN copy
                # made from a non-browser request would then break browser clients.
                response.headers.setdefault("Access-Control-Allow-Origin", "*")
    return response


# Include API routers (MUST be before static files)
app.include_router(health.router)
app.include_router(nowcast.router)
app.include_router(earthquake.router)
app.include_router(weather.router)
app.include_router(wilayah.router)

def _redirect_to(target: str):
    async def redirect():
        return RedirectResponse(target, status_code=301)

    return redirect


# Website pages live at a trailing-slash URL. Redirect the old .html names and
# the bare names here, with a relative Location: behind a TLS-terminating proxy
# the app sees plain HTTP, and the absolute URL StaticFiles would build for a
# bare name points at http://.
WEBSITE_REDIRECTS = {
    "/self-host.html": "/self-host/",
    "/mcp-setup.html": "/mcp-setup/",
    "/docs": "/docs/",
    "/self-host": "/self-host/",
    "/mcp-setup": "/mcp-setup/",
    # English pages live under /en
    "/en": "/en/",
    "/en/docs": "/en/docs/",
    "/en/self-host": "/en/self-host/",
    "/en/mcp-setup": "/en/mcp-setup/",
}
for _old, _new in WEBSITE_REDIRECTS.items():
    app.add_api_route(_old, _redirect_to(_new), include_in_schema=False)


# Mount the website (MUST be last due to catch-all behavior). The directory is
# produced by the web/ build, so it may be absent when only the API is run.
app.mount("/", StaticFiles(directory=settings.landing_dir, html=True, check_dir=False), name="landing")


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_error",
            "message": "An unexpected error occurred",
            "status": 500,
        },
    )
