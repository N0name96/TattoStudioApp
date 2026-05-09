"""Query to list payments with optional filters."""

import logging
from uuid import UUID

from application.dto.responses.payments.payment_response import (
    PaymentResponse,
)
from domain.enums.payment_status import PaymentStatus
from domain.repositories.payment_repository import PaymentRepository

logger = logging.getLogger(__name__)


class ListPaymentsQuery:
    """Query to list payments with optional filters.

    This query handles listing payment records, supporting
    filtering by appointment or by payment status.

    Attributes:
        _payment_repo: Repository for payment lookups.
    """

    def __init__(self, payment_repo: PaymentRepository) -> None:
        """Initialize the query with the payment repository.

        Args:
            payment_repo: Repository for payment lookups.
        """

        self._payment_repo = payment_repo


    async def execute(
        self,
        appointment_id: UUID | None = None,
        status: PaymentStatus | None = None,
    ) -> list[PaymentResponse]:
        """Execute the payment listing.

        Args:
            appointment_id: Optional filter by appointment UUID.
            status: Optional filter by payment status.

        Returns:
            A list of payment response DTOs.
        """

        if appointment_id is not None:
            payments = await self._payment_repo.list_by_appointment(appointment_id)
        else:
            payments = await self._payment_repo.list_all(status=status)

        return [PaymentResponse.model_validate(p) for p in payments]
