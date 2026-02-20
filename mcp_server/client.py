import httpx
import logging
from typing import Optional

BASE_URL = "https://bmkg-restapi.vercel.app/v1"
TIMEOUT = 30.0

logger = logging.getLogger("mcp_server.client")


class BMKGClient:
    """Singleton async HTTP client for BMKG API."""

    _instance: Optional["BMKGClient"] = None
    _client: Optional[httpx.AsyncClient] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def get(self, endpoint: str, params: dict = None) -> dict:
        """Make GET request to BMKG API."""
        if self._client is None:
            self._client = httpx.AsyncClient(base_url=BASE_URL, timeout=TIMEOUT)
        
        logger.debug(f"HTTP GET {endpoint} params={params}")
        
        response = await self._client.get(endpoint, params=params)
        
        logger.debug(f"HTTP Response {response.status_code} for {endpoint}")
        
        response.raise_for_status()
        return response.json()

    async def close(self):
        """Close the client connection."""
        if self._client:
            await self._client.aclose()
            self._client = None


# Global client instance
client = BMKGClient()
