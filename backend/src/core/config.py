"""Application configuration using pydantic-settings.

This module provides type-safe configuration management through
environment variables. Settings are loaded from .env files and
environment variables automatically.

Usage:
    from core.config import settings

    db_url = settings.SUPABASE_URL
"""

from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables.

    All configuration is centralized here. Values can be set via:
    - Environment variables
    - .env file in the project root
    - Default values (for development)

    Attributes:
        APP_NAME: Application name for logging and docs.
        DEBUG: Enable debug mode (verbose logging).
        SUPABASE_URL: Supabase project URL.
        SUPABASE_KEY: Supabase anonymous/public key.
        SUPABASE_SERVICE_KEY: Supabase service role key (for admin operations).
        SECRET_KEY: Secret key for JWT signing.
        JWT_ALGORITHM: Algorithm used for JWT tokens.
        JWT_ACCESS_TOKEN_EXPIRE_MINUTES: Access token validity in minutes.
        JWT_REFRESH_TOKEN_EXPIRE_DAYS: Refresh token validity in days.
        REDIS_URL: Redis connection URL for Celery and caching.
        LOG_LEVEL: Logging level (DEBUG, INFO, WARNING, ERROR).
    """

    # Application
    APP_NAME: str = "TattoStudioApp"
    DEBUG: bool = False

    # Supabase
    SUPABASE_URL: str = "https://mczwgmvuauijbbmpzxip.supabase.co"
    SUPABASE_KEY: str = "sb_publishable_TJClDWc1GWPmQu45sKj5Qg_B0b_ksBZ"
    SUPABASE_SERVICE_KEY: str = (
        "VKFDV8b3ILB5PW0+1wdV3VgOLhU2WtSGvw7J4qjQNrJb+fhSj16ltKhPbMlSWYPh3Y5UvVC8nupDUTWf4FWVGg=="
    )

    # Security
    SECRET_KEY: str = "change-me-in-production"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"

    # Logging
    LOG_LEVEL: str = "INFO"

    model_config = ConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


# Global settings instance
settings = Settings()
