"""Stable response envelope and error codes shared by every MCP tool."""

import logging
import uuid
from time import perf_counter
from typing import Any, Literal

import httpx
from pydantic import BaseModel, Field

from mcp_server import __version__
from mcp_server import cache as tool_cache
from mcp_server.client import client

logger = logging.getLogger("mcp_server.tools")

# Machine-readable error codes. Messages are fixed and safe to show: exception
# text, URLs and stack traces never reach the caller.
ERROR_MESSAGES = {
    "INVALID_ARGUMENT": "The request was rejected as invalid. Check the argument formats in the tool description.",
    "NOT_FOUND": "No data was found for that input.",
    "RATE_LIMITED": "Too many requests. Wait a minute before trying again.",
    "UPSTREAM_UNAVAILABLE": "BMKG data is temporarily unavailable. Try again shortly.",
    "INTERNAL_ERROR": "The server could not complete the request.",
}


class ErrorDetail(BaseModel):
    """Why a tool call failed."""

    code: str = Field(description="Stable error code: " + ", ".join(ERROR_MESSAGES))
    message: str = Field(description="Explanation that is safe to show to a user")


class ResponseMeta(BaseModel):
    """How a tool result was produced."""

    tool_version: str = Field(description="Version of the MCP server")
    operation: str = Field(description="Name of the tool that ran")
    trace_id: str = Field(description="Identifier of this call in the server logs")
    latency_ms: float = Field(description="Time spent on the call", ge=0)
    source: str | None = Field(default=None, description="Who owns the data; cite it when reporting results")
    fetched_at: str | None = Field(default=None, description="When the data was read from the source (UTC)")
    cache_ttl_seconds: int | None = Field(default=None, description="Seconds until the source is asked again")
    served_from_cache: bool = Field(default=False, description="True if this server answered from its own cache")
    details: dict[str, Any] = Field(default_factory=dict, description="Extra facts about the result, such as count")
    warnings: list[str] = Field(default_factory=list, description="Caveats about this result")


class ToolResponse(BaseModel):
    """Envelope returned by every tool: check `status` first."""

    status: Literal["success", "error"]
    data: Any | None = Field(default=None, description="The result; null when status is error")
    error: ErrorDetail | None = Field(default=None, description="The failure; null when status is success")
    meta: ResponseMeta


def classify(exc: Exception) -> str:
    """Map an exception to an error code."""
    if isinstance(exc, httpx.HTTPStatusError):
        status = exc.response.status_code
        if status in (400, 422):
            return "INVALID_ARGUMENT"
        if status == 404:
            return "NOT_FOUND"
        if status == 429:
            return "RATE_LIMITED"
        if status >= 500:
            return "UPSTREAM_UNAVAILABLE"
    if isinstance(exc, httpx.HTTPError):
        # Timeouts and connection failures
        return "UPSTREAM_UNAVAILABLE"
    return "INTERNAL_ERROR"


async def call_api(
    operation: str,
    endpoint: str,
    params: dict[str, Any] | None = None,
    *,
    cache_type: str,
    not_found: str | None = None,
) -> ToolResponse:
    """Run one tool call against the BMKG API and wrap the outcome.

    Args:
        operation: Tool name, reported in meta and logs
        endpoint: API path below /v1
        params: Query parameters
        cache_type: Which cache TTL applies (see mcp_server.cache.CACHE_TTL)
        not_found: Message for NOT_FOUND that tells the caller what to try instead
    """
    trace_id = uuid.uuid4().hex
    started = perf_counter()

    def meta(**fields: Any) -> ResponseMeta:
        return ResponseMeta(
            tool_version=__version__,
            operation=operation,
            trace_id=trace_id,
            latency_ms=round((perf_counter() - started) * 1000, 1),
            **fields,
        )

    try:
        payload, from_cache = await tool_cache.get_or_fetch(
            cache_type, endpoint, params, lambda: client.get(endpoint, params=params)
        )
    except Exception as exc:
        code = classify(exc)
        logger.warning(
            "%s failed: %s trace_id=%s cause=%r",
            operation, code, trace_id, exc,
            exc_info=code == "INTERNAL_ERROR",
        )
        message = not_found if code == "NOT_FOUND" and not_found else ERROR_MESSAGES[code]
        return ToolResponse(status="error", error=ErrorDetail(code=code, message=message), meta=meta())

    api_meta = dict(payload.get("meta") or {})
    return ToolResponse(
        status="success",
        data=payload.get("data"),
        meta=meta(
            source=payload.get("attribution"),
            fetched_at=api_meta.pop("fetched_at", None),
            cache_ttl_seconds=api_meta.pop("cache_ttl", None),
            served_from_cache=from_cache,
            details=api_meta,
        ),
    )
