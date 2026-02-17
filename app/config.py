"""Application configuration using pydantic-settings."""

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    
    # Server
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8099, alias="PORT")
    
    # Redis
    redis_url: str = Field(default="redis://localhost:6379", alias="REDIS_URL")
    
    # Rate Limiting
    rate_limit_anonymous: str = Field(default="30/minute", alias="RATE_LIMIT_ANONYMOUS")
    rate_limit_authenticated: str = Field(default="120/minute", alias="RATE_LIMIT_AUTHENTICATED")
    
    # Cache TTL (seconds)
    cache_ttl_nowcast: int = Field(default=120, alias="CACHE_TTL_NOWCAST")
    cache_ttl_weather: int = Field(default=900, alias="CACHE_TTL_WEATHER")
    cache_ttl_earthquake_latest: int = Field(default=60, alias="CACHE_TTL_EARTHQUAKE_LATEST")
    cache_ttl_earthquake_list: int = Field(default=300, alias="CACHE_TTL_EARTHQUAKE_LIST")
    
    # API Keys (comma-separated)
    api_keys: str = Field(default="", alias="API_KEYS")
    
    # BMKG Base URLs
    bmkg_nowcast_base_url: str = Field(
        default="https://www.bmkg.go.id/alerts/nowcast",
        alias="BMKG_NOWCAST_BASE_URL"
    )
    bmkg_weather_base_url: str = Field(
        default="https://api.bmkg.go.id/publik",
        alias="BMKG_WEATHER_BASE_URL"
    )
    bmkg_earthquake_base_url: str = Field(
        default="https://data.bmkg.go.id/DataMKG/TEWS",
        alias="BMKG_EARTHQUAKE_BASE_URL"
    )
    
    # Logging
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    
    @property
    def api_key_list(self) -> list[str]:
        """Return list of valid API keys."""
        if not self.api_keys:
            return []
        return [key.strip() for key in self.api_keys.split(",") if key.strip()]


# Global settings instance
settings = Settings()
