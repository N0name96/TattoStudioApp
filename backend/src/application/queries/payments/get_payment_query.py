"""Query to retrieve a single payment by ID."""

import logging
from uuid import UUID

from application.dto.responses.payments.payment_response import (
    PaymentResponse,
)
from domain.repositories.payment_repository import PaymentRepository
from core.errors import EntityNotFoundError

logger = logging.getLogger(__name__)


class GetPaymentQuery:
    """Query to retrieve a single payment by ID.

    This query handles the read operation for payment data,
    mapping from domain entity to response DTO.

    Attributes:
        _payment_repo: Repository for payment lookups.
    """

    def __init__(self, payment_repo: PaymentRepository) -> None:
        """Initialize the query with the payment repository.

        Args:
            payment_repo: Repository for payment lookups.
        """

        self._payment_repo = payment_repo


    async def execute(self, payment_id: UUID) -> PaymentResponse:
        """Execute the payment retrieval.

        Args:
            payment_id: The unique identifier of the payment.

        Returns:
            The payment data as a response DTO.

        Raises:
            EntityNotFoundError: If the payment does not exist.
        """

        payment = await self._payment_repo.get_by_id(payment_id)

        if payment is None:
            raise EntityNotFoundError(f"Payment {payment_id} not found")

        return PaymentResponse.model_validate(payment)
