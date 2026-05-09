"""In-memory payment repository for development and testing.

This module provides a simple in-memory implementation of the
PaymentRepository protocol. Stores payments in a dictionary,
useful for rapid development and unit testing.

Note: Data is NOT persisted between restarts. For production,
use the Supabase repository implementation.
"""

from uuid import UUID

from domain.entities.payment_entity import Payment
from domain.enums.payment_status import PaymentStatus
from domain.repositories.payment_repository import PaymentRepository


class InMemoryPaymentRepository:
    """In-memory implementation of PaymentRepository.

    Stores Payment entities in a dictionary keyed by payment ID.
    Implements all methods defined by the PaymentRepository protocol.

    Attributes:
        _storage: Internal dictionary storing Payment entities.
    """

    def __init__(self) -> None:
        """Initialize with an empty payment store."""

        self._storage: dict[UUID, Payment] = {}


    async def get_by_id(self, payment_id: UUID) -> Payment | None:
        """Retrieve a payment by its unique identifier.

        Args:
            payment_id: The UUID of the payment to find.

        Returns:
            The Payment entity if found, None otherwise.
        """

        return self._storage.get(payment_id)


    async def save(self, payment: Payment) -> Payment:
        """Persist a payment entity (create or update).

        If the payment ID already exists, it is updated in place.
        Otherwise, it is stored as a new payment.

        Args:
            payment: The Payment entity to persist.

        Returns:
            The persisted Payment entity.
        """

        self._storage[payment.id] = payment

        return payment


    async def list_by_appointment(
        self,
        appointment_id: UUID,
    ) -> list[Payment]:
        """List all payments for a specific appointment.

        Args:
            appointment_id: The UUID of the appointment.

        Returns:
            A list of Payment entities for the appointment.
        """

        return [
            p
            for p in self._storage.values()
            if p.appointment_id == appointment_id
        ]


    async def find_by_stripe_id(
        self,
        stripe_payment_id: str,
    ) -> Payment | None:
        """Find a payment by its Stripe payment ID.

        Args:
            stripe_payment_id: The Stripe payment intent ID.

        Returns:
            The Payment entity if found, None otherwise.
        """

        for payment in self._storage.values():
            if payment.stripe_payment_id == stripe_payment_id:
                return payment

        return None


    async def list_all(
        self,
        status: PaymentStatus | None = None,
    ) -> list[Payment]:
        """List all payments in the system.

        Args:
            status: Optional filter by payment status.

        Returns:
            A list of all Payment entities, optionally filtered.
        """

        payments = list(self._storage.values())

        if status is not None:
            payments = [p for p in payments if p.status == status]

        return payments
