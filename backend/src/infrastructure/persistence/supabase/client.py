"""Supabase client singleton for the TattoStudioApp.

Provides a single shared Supabase client instance across all
repository implementations, ensuring only one connection pool
is created per application lifecycle.
"""

import logging

from supabase import AsyncClient

from core.errors import DatabaseError

logger = logging.getLogger(__name__)


class SupabaseClientSingleton:
    """Singleton for managing the Supabase client instance.

    Ensures only one client instance is created and reused
    across the application lifecycle.
    """

    _instance: AsyncClient | None = None


    @classmethod
    async def get_client(cls) -> AsyncClient:
        """Get or create the Supabase client instance.

        Returns:
            The configured async Supabase client.

        Raises:
            DatabaseError: If connection fails.
        """

        if cls._instance is None:
            try:
                from supabase import create_client

                from core.config import settings

                cls._instance = create_client(
                    supabase_url=settings.SUPABASE_URL,
                    supabase_key=settings.SUPABASE_KEY,
                )
                logger.info("Supabase client initialized")
            except Exception as e:
                raise DatabaseError(f"Failed to connect to Supabase: {e}")

        return cls._instance
