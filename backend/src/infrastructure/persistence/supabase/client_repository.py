"""Supabase implementation of the ClientRepository."""

import logging
from uuid import UUID

from core.errors import DatabaseError
from domain.entities.client_entity import Client
from infrastructure.persistence.supabase.client import SupabaseClientSingleton
from infrastructure.persistence.supabase.mappers import map_to_client, map_to_client_dict

logger = logging.getLogger(__name__)

TABLE = "clients"


class SupabaseClientRepository:
    TABLE = TABLE

    async def get_by_id(self, client_id: UUID) -> Client | None:
        try:
            client = await SupabaseClientSingleton.get_client()
            response = client.table(self.TABLE).select("*").eq("id", str(client_id)).execute()
            if not response.data:
                return None
            return map_to_client(response.data[0])
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to get client: {e}")

    async def get_by_email(self, email: str) -> Client | None:
        try:
            client = await SupabaseClientSingleton.get_client()
            response = client.table(self.TABLE).select("*").eq("email", email).execute()
            if not response.data:
                return None
            return map_to_client(response.data[0])
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to get client by email: {e}")

    async def save(self, client: Client) -> Client:
        try:
            supabase_client = await SupabaseClientSingleton.get_client()
            data = map_to_client_dict(client)
            response = supabase_client.table(self.TABLE).upsert(data).execute()
            if not response.data:
                raise DatabaseError("Failed to save client: no data returned")
            return map_to_client(response.data[0])
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to save client: {e}")

    async def list_all(self, active_only: bool = True) -> list[Client]:
        try:
            supabase_client = await SupabaseClientSingleton.get_client()
            query = supabase_client.table(self.TABLE).select("*").order("created_at", desc=True)
            if active_only:
                query = query.eq("is_active", True)
            response = query.execute()
            return [map_to_client(row) for row in response.data]
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to list clients: {e}")

    async def delete(self, client_id: UUID) -> None:
        try:
            supabase_client = await SupabaseClientSingleton.get_client()
            supabase_client.table(self.TABLE).delete().eq("id", str(client_id)).execute()
        except Exception as e:
            raise DatabaseError(f"Failed to delete client: {e}")
