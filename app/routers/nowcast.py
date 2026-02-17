"""Nowcast (weather warnings) API routes."""

from datetime import datetime, timezone
from fastapi import APIRouter, Query, Request, Depends, HTTPException
from fastapi.responses import JSONResponse

from app.config import settings
from app.dependencies import limiter
from app.models.nowcast import (
    ActiveProvince,
    Warning,
    LocationCheckResult,
    NowcastDetailResponse,
    NowcastMeta,
)
from app.models.responses import APIResponse
from app.services.nowcast_service import nowcast_service

router = APIRouter(
    prefix="/v1/nowcast",
    tags=["nowcast"],
)


def serialize_warning(warning: Warning) -> dict:
    """Serialize warning to dict for API response."""
    data = warning.model_dump(mode='json')
    # Ensure datetime fields are properly formatted
    if warning.effective:
        data['effective'] = warning.effective.isoformat() if warning.effective.tzinfo else warning.effective.isoformat() + "+00:00"
    if warning.expires:
        data['expires'] = warning.expires.isoformat() if warning.expires.tzinfo else warning.expires.isoformat() + "+00:00"
    return data


@router.get("", response_model=APIResponse[list[ActiveProvince]])
@limiter.limit(settings.rate_limit_anonymous)
async def get_active_provinces(
    request: Request,
    lang: str = Query("id", description="Language code (id/en)", pattern="^(id|en)$"),
):
    """Get provinces with active weather warnings.
    
    Returns a list of provinces that currently have active weather warnings.
    Data is fetched from BMKG's RSS feed and cached for 120 seconds.
    
    **Query Parameters:**
    - `lang`: Language code - "id" (Indonesian) or "en" (English). Default: "id"
    """
    try:
        provinces, from_cache, ttl = await nowcast_service.get_active_provinces(lang)
        
        response_data = {
            "data": [p.model_dump(mode='json') for p in provinces],
            "meta": {
                "count": len(provinces),
                "fetched_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "cache_ttl": ttl,
                "language": lang,
            },
            "attribution": "BMKG (Badan Meteorologi, Klimatologi, dan Geofisika)",
        }
        
        headers = {
            "X-Cache": "HIT" if from_cache else "MISS",
            "X-Cache-TTL": str(ttl),
        }
        
        return JSONResponse(content=response_data, headers=headers)
        
    except Exception as e:
        return JSONResponse(
            status_code=502,
            content={
                "error": "upstream_error",
                "message": f"Failed to fetch weather warnings: {str(e)}",
                "status": 502,
            },
        )


@router.get("/{alert_code}", response_model=APIResponse[NowcastDetailResponse])
@limiter.limit(settings.rate_limit_anonymous)
async def get_warning_detail(
    request: Request,
    alert_code: str,
    lang: str = Query("id", description="Language code (id/en)", pattern="^(id|en)$"),
):
    """Get detailed weather warning for an alert.
    
    Returns detailed CAP (Common Alerting Protocol) data for a specific alert,
    including affected areas with polygon coordinates.
    
    **Path Parameters:**
    - `alert_code`: Alert code from the RSS feed (e.g., 'CBT20260216004')
    
    **Query Parameters:**
    - `lang`: Language code - "id" (Indonesian) or "en" (English). Default: "id"
    """
    try:
        warning, region_name, from_cache, ttl = await nowcast_service.get_warning_detail(
            alert_code, lang
        )
        
        if warning is None:
            return JSONResponse(
                status_code=404,
                content={
                    "error": "not_found",
                    "message": f"Alert '{alert_code}' not found or no longer active",
                    "status": 404,
                },
            )
        
        response_data = {
            "data": {
                "province": region_name,
                "warnings": [serialize_warning(warning)],
            },
            "meta": {
                "count": 1,
                "fetched_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "cache_ttl": ttl,
                "language": lang,
            },
            "attribution": "BMKG (Badan Meteorologi, Klimatologi, dan Geofisika)",
        }
        
        headers = {
            "X-Cache": "HIT" if from_cache else "MISS",
            "X-Cache-TTL": str(ttl),
        }
        
        return JSONResponse(content=response_data, headers=headers)
        
    except Exception as e:
        return JSONResponse(
            status_code=502,
            content={
                "error": "upstream_error",
                "message": f"Failed to fetch warning detail: {str(e)}",
                "status": 502,
            },
        )


@router.get("/check", response_model=APIResponse[LocationCheckResult])
@limiter.limit(settings.rate_limit_anonymous)
async def check_location_warnings(
    request: Request,
    location: str = Query(..., description="Kecamatan/district name to check (e.g., 'Wiradesa', 'Bojonegara')"),
    lang: str = Query("id", description="Language code (id/en)", pattern="^(id|en)$"),
):
    """Check weather warnings for a specific location.
    
    Searches all active weather warnings for mentions of the given location.
    Performs case-insensitive matching in warning descriptions.
    
    **Query Parameters:**
    - `location`: Location name (kecamatan/district) to search for. **Required**
    - `lang`: Language code - "id" (Indonesian) or "en" (English). Default: "id"
    
    **Example:**
    - `/v1/nowcast/check?location=Bojonegara`
    - `/v1/nowcast/check?location=Wiradesa&lang=id`
    """
    if not location or not location.strip():
        return JSONResponse(
            status_code=400,
            content={
                "error": "bad_request",
                "message": "Location parameter is required",
                "status": 400,
            },
        )
    
    try:
        result, from_cache, ttl = await nowcast_service.check_location(location.strip(), lang)
        
        response_data = {
            "data": result.model_dump(mode='json'),
            "meta": {
                "location": location.strip(),
                "checked_provinces": len(result.warnings),
                "fetched_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                "cache_ttl": ttl,
                "language": lang,
            },
            "attribution": "BMKG (Badan Meteorologi, Klimatologi, dan Geofisika)",
        }
        
        headers = {
            "X-Cache": "HIT" if from_cache else "MISS",
            "X-Cache-TTL": str(ttl),
        }
        
        return JSONResponse(content=response_data, headers=headers)
        
    except Exception as e:
        return JSONResponse(
            status_code=502,
            content={
                "error": "upstream_error",
                "message": f"Failed to check location warnings: {str(e)}",
                "status": 502,
            },
        )
