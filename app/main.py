"""Main FastAPI application."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.config import settings
from app.cache import cache
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
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
    lifespan=lifespan,
    openapi_tags=TAGS_METADATA,
    contact={
        "name": "Dhany",
        "url": "https://github.com/dhanypedia/bmkg-api",
    },
    license_info={
        "name": "MIT",
        "url": "https://opensource.org/licenses/MIT",
    },
)

# Add rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

# Include API routers (MUST be before static files)
app.include_router(health.router)
app.include_router(nowcast.router)
app.include_router(earthquake.router)
app.include_router(weather.router)
app.include_router(wilayah.router)

# Mount static files for landing page (MUST be last due to catch-all behavior)
app.mount("/static", StaticFiles(directory="landing"), name="static")
app.mount("/", StaticFiles(directory="landing", html=True), name="landing")


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
