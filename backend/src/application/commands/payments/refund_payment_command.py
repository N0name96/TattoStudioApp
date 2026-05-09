"""Command to refund a payment in the TattoStudioApp.

This command handles the refund flow:
1. Retrieve the payment by ID
2. Apply the refund transition on the domain entity
3. Persist the updated entity
"""

import logging
from uuid import UUID

from application.dto.responses.payments.payment_response import (
    PaymentResponse,
)
from domain.repositories.payment_repository import PaymentRepository
from core.errors import EntityNotFoundError

logger = logging.getLogger(__name__)


class RefundPaymentCommand:
    """Command to refund an existing payment.

    This command applies the refund transition on the domain entity.

    Note: Stripe refund processing is handled by the use case,
    not by this command.

    Attributes:
        _payment_repo: Repository for payment persistence.
    """

    def __init__(self, payment_repo: PaymentRepository) -> None:
        """Initialize the command with the payment repository.

        Args:
            payment_repo: Repository for payment persistence.
        """

        self._payment_repo = payment_repo


    async def execute(self, payment_id: UUID) -> PaymentResponse:
        """Execute the payment refund flow.

        Steps:
            1. Retrieve the payment.
            2. Apply the refund transition on the domain entity.
            3. Persist the updated entity.

        Args:
            payment_id: UUID of the payment to refund.

        Returns:
            The updated payment as a response DTO.

        Raises:
            EntityNotFoundError: If the payment does not exist.
        """

        logger.info(
            "Refunding payment",
            extra={"extra_data": {"payment_id": str(payment_id)}},
        )

        # Step 1: Retrieve the payment
        payment = await self._payment_repo.get_by_id(payment_id)

        if payment is None:
            raise EntityNotFoundError(
                f"Payment {payment_id} not found"
            )

        # Step 2: Apply the refund transition
        payment.refund()

        # Step 3: Persist the updated entity
        saved = await self._payment_repo.save(payment)

        logger.info(
            "Payment refunded successfully",
            extra={"extra_data": {"payment_id": str(saved.id)}},
        )

        return PaymentResponse.model_validate(saved)
