"""Payment repository interface (Protocol) for the TattoStudioApp.

This module defines the contract that any payment repository
implementation must satisfy. It uses Python's Protocol for structural
subtyping, allowing any class with matching methods to be used.

Implemented by:
    - infrastructure/persistence/supabase/payment_repository.py
    - infrastructure/persistence/in_memory/payment_repository.py
"""

from typing import Protocol, runtime_checkable
from uuid import UUID

from domain.entities.payment_entity import Payment
from domain.enums.payment_status import PaymentStatus


@runtime_checkable
class PaymentRepository(Protocol):
    """Interface for Payment persistence.

    This protocol defines the contract that any payment repository
    implementation must satisfy. It is implemented in the Infrastructure
    layer.

    The @runtime_checkable decorator allows isinstance() checks.
    """

    async def get_by_id(self, payment_id: UUID) -> Payment | None:
        """Retrieve a payment by its unique identifier.

        Args:
            payment_id: The UUID of the payment to find.

        Returns:
            The Payment entity if found, None otherwise.
        """
        ...


    async def save(self, payment: Payment) -> Payment:
        """Persist a payment entity (create or update).

        Uses upsert semantics: creates if new, updates if exists.

        Args:
            payment: The Payment entity to persist.

        Returns:
            The persisted Payment entity.
        """
        ...


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
        ...


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
        ...


    async def list_all(
        self,
        status: PaymentStatus | None = None,
    ) -> list[Payment]:
        """List all payments in the system.

        Args:
            status: Optional filter by payment status.

        Returns:
            A list of all Payment entities.
        """
        ...
