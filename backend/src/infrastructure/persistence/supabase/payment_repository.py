"""Supabase implementation of the PaymentRepository."""

import logging
from uuid import UUID

from core.errors import DatabaseError
from domain.entities.payment_entity import Payment
from domain.enums.payment_status import PaymentStatus
from infrastructure.persistence.supabase.client import SupabaseClientSingleton
from infrastructure.persistence.supabase.mappers import map_to_payment, map_to_payment_dict

logger = logging.getLogger(__name__)

TABLE = "payments"


class SupabasePaymentRepository:
    TABLE = TABLE

    async def get_by_id(self, payment_id: UUID) -> Payment | None:
        try:
            client = await SupabaseClientSingleton.get_client()
            response = client.table(self.TABLE).select("*").eq("id", str(payment_id)).execute()
            if not response.data:
                return None
            return map_to_payment(response.data[0])
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to get payment: {e}")

    async def save(self, payment: Payment) -> Payment:
        try:
            client = await SupabaseClientSingleton.get_client()
            data = map_to_payment_dict(payment)
            response = client.table(self.TABLE).upsert(data).execute()
            if not response.data:
                raise DatabaseError("Failed to save payment: no data returned")
            return map_to_payment(response.data[0])
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to save payment: {e}")

    async def list_by_appointment(self, appointment_id: UUID) -> list[Payment]:
        try:
            client = await SupabaseClientSingleton.get_client()
            response = (
                client.table(self.TABLE)
                .select("*")
                .eq("appointment_id", str(appointment_id))
                .order("created_at", desc=True)
                .execute()
            )
            return [map_to_payment(row) for row in response.data]
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to list payments: {e}")

    async def find_by_stripe_id(self, stripe_payment_id: str) -> Payment | None:
        try:
            client = await SupabaseClientSingleton.get_client()
            response = client.table(self.TABLE).select("*").eq("stripe_payment_id", stripe_payment_id).execute()
            if not response.data:
                return None
            return map_to_payment(response.data[0])
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to find payment by stripe id: {e}")

    async def list_all(self, status: PaymentStatus | None = None) -> list[Payment]:
        try:
            client = await SupabaseClientSingleton.get_client()
            query = client.table(self.TABLE).select("*").order("created_at", desc=True)
            if status is not None:
                query = query.eq("status", status.value)
            response = query.execute()
            return [map_to_payment(row) for row in response.data]
        except DatabaseError:
            raise
        except Exception as e:
            raise DatabaseError(f"Failed to list payments: {e}")
