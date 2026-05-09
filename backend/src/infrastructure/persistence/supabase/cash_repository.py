"""Supabase implementation of the CashRepository."""

import logging
from uuid import UUID

from core.errors import DatabaseError
from domain.entities.cash_transaction_entity import CashTransaction
from domain.enums.cash_transaction_type import CashTransactionType
from infrastructure.persistence.supabase.client import SupabaseClientSingleton
from infrastructure.persistence.supabase.mappers import map_to_cash_transaction, map_to_cash_transaction_dict

logger = logging.getLogger(__name__)

TABLE = "cash_transactions"


class SupabaseCashRepository:
    TABLE = TABLE

    async def get_by_id(self, transaction_id: UUID) -> CashTransaction | None:
        try:
            client = await SupabaseClientSingleton.get_client()
            response = client.table(self.TABLE).select("*").eq("id", str(transaction_id)).execute()
            if not response.data:
                return None
            return map_to_cash_transaction(response.data[0])
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to get cash transaction: {e}")

    async def save(self, transaction: CashTransaction) -> CashTransaction:
        try:
            client = await SupabaseClientSingleton.get_client()
            data = map_to_cash_transaction_dict(transaction)
            response = client.table(self.TABLE).upsert(data).execute()
            if not response.data:
                raise DatabaseError("Failed to save cash transaction: no data returned")
            return map_to_cash_transaction(response.data[0])
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to save cash transaction: {e}")

    async def list_all(
        self,
        transaction_type: CashTransactionType | None = None,
    ) -> list[CashTransaction]:
        try:
            client = await SupabaseClientSingleton.get_client()
            query = client.table(self.TABLE).select("*").order("created_at", desc=True)
            if transaction_type is not None:
                query = query.eq("transaction_type", transaction_type.value)
            response = query.execute()
            return [map_to_cash_transaction(row) for row in response.data]
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to list cash transactions: {e}")

    async def list_by_appointment(self, appointment_id: UUID) -> list[CashTransaction]:
        try:
            client = await SupabaseClientSingleton.get_client()
            response = (
                client.table(self.TABLE)
                .select("*")
                .eq("appointment_id", str(appointment_id))
                .order("created_at", desc=True)
                .execute()
            )
            return [map_to_cash_transaction(row) for row in response.data]
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to list cash transactions: {e}")

    async def delete(self, transaction_id: UUID) -> None:
        try:
            client = await SupabaseClientSingleton.get_client()
            client.table(self.TABLE).delete().eq("id", str(transaction_id)).execute()
        except Exception as e:
            raise DatabaseError(f"Failed to delete cash transaction: {e}")
