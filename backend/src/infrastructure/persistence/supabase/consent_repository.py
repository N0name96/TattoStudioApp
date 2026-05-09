"""Supabase implementation of the ConsentRepository."""

import logging
from uuid import UUID

from core.errors import DatabaseError
from domain.entities.consent_entity import Consent
from domain.enums.consent_status import ConsentStatus
from infrastructure.persistence.supabase.client import SupabaseClientSingleton
from infrastructure.persistence.supabase.mappers import map_to_consent, map_to_consent_dict

logger = logging.getLogger(__name__)

TABLE = "consents"


class SupabaseConsentRepository:
    TABLE = TABLE

    async def get_by_id(self, consent_id: UUID) -> Consent | None:
        try:
            client = await SupabaseClientSingleton.get_client()
            response = client.table(self.TABLE).select("*").eq("id", str(consent_id)).execute()
            if not response.data:
                return None
            return map_to_consent(response.data[0])
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to get consent: {e}")

    async def save(self, consent: Consent) -> Consent:
        try:
            client = await SupabaseClientSingleton.get_client()
            data = map_to_consent_dict(consent)
            response = client.table(self.TABLE).upsert(data).execute()
            if not response.data:
                raise DatabaseError("Failed to save consent: no data returned")
            return map_to_consent(response.data[0])
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to save consent: {e}")

    async def find_by_token(self, token: str) -> Consent | None:
        try:
            client = await SupabaseClientSingleton.get_client()
            response = client.table(self.TABLE).select("*").eq("token", token).execute()
            if not response.data:
                return None
            return map_to_consent(response.data[0])
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to find consent by token: {e}")

    async def list_by_client(
        self,
        client_id: UUID,
        status: ConsentStatus | None = None,
    ) -> list[Consent]:
        try:
            client = await SupabaseClientSingleton.get_client()
            query = client.table(self.TABLE).select("*").eq("client_id", str(client_id))
            if status is not None:
                query = query.eq("status", status.value)
            response = query.order("created_at", desc=True).execute()
            return [map_to_consent(row) for row in response.data]
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to list consents: {e}")

    async def list_all(
        self,
        client_id: UUID | None = None,
        status: ConsentStatus | None = None,
    ) -> list[Consent]:
        try:
            client = await SupabaseClientSingleton.get_client()
            query = client.table(self.TABLE).select("*")
            if client_id is not None:
                query = query.eq("client_id", str(client_id))
            if status is not None:
                query = query.eq("status", status.value)
            response = query.order("created_at", desc=True).execute()
            return [map_to_consent(row) for row in response.data]
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to list consents: {e}")
