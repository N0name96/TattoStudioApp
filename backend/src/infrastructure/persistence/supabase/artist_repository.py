"""Supabase implementation of the ArtistRepository."""

import logging
from uuid import UUID

from core.errors import DatabaseError
from domain.entities.artist_entity import Artist
from infrastructure.persistence.supabase.client import SupabaseClientSingleton
from infrastructure.persistence.supabase.mappers import map_to_artist, map_to_artist_dict

logger = logging.getLogger(__name__)

TABLE = "artists"


class SupabaseArtistRepository:
    TABLE = TABLE

    async def get_by_id(self, artist_id: UUID) -> Artist | None:
        try:
            client = await SupabaseClientSingleton.get_client()
            response = client.table(self.TABLE).select("*").eq("id", str(artist_id)).execute()
            if not response.data:
                return None
            return map_to_artist(response.data[0])
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to get artist: {e}")

    async def get_all(self, active_only: bool = True) -> list[Artist]:
        try:
            client = await SupabaseClientSingleton.get_client()
            query = client.table(self.TABLE).select("*")
            if active_only:
                query = query.eq("is_active", True)
            response = query.execute()
            return [map_to_artist(row) for row in response.data]
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to list artists: {e}")

    async def save(self, artist: Artist) -> Artist:
        try:
            client = await SupabaseClientSingleton.get_client()
            data = map_to_artist_dict(artist)
            response = client.table(self.TABLE).upsert(data).execute()
            if not response.data:
                raise DatabaseError("Failed to save artist: no data returned")
            return map_to_artist(response.data[0])
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to save artist: {e}")

    async def delete(self, artist_id: UUID) -> None:
        try:
            client = await SupabaseClientSingleton.get_client()
            client.table(self.TABLE).delete().eq("id", str(artist_id)).execute()
        except Exception as e:
            raise DatabaseError(f"Failed to delete artist: {e}")

    async def find_by_user_id(self, user_id: UUID) -> Artist | None:
        try:
            client = await SupabaseClientSingleton.get_client()
            response = client.table(self.TABLE).select("*").eq("user_id", str(user_id)).execute()
            if not response.data:
                return None
            return map_to_artist(response.data[0])
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to find artist: {e}")
