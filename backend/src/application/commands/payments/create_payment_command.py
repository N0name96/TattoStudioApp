"""Command to create a new payment in the TattoStudioApp.

This command handles the payment creation flow:
1. Verify the associated appointment exists
2. Create the domain entity with business rules
3. Persist to repository
4. Return response DTO

Stripe processing is handled separately by the PaymentUseCase
which orchestrates this command with the Stripe service.
"""

import logging
from uuid import UUID

from application.dto.requests.payments.create_payment_request import (
    CreatePaymentRequest,
)
from application.dto.responses.payments.payment_response import (
    PaymentResponse,
)
from domain.entities.payment_entity import Payment
from domain.repositories.appointment_repository import AppointmentRepository
from domain.repositories.payment_repository import PaymentRepository
from core.errors import EntityNotFoundError

logger = logging.getLogger(__name__)


class CreatePaymentCommand:
    """Command to create a new payment in the system.

    This command validates the request, verifies the appointment exists,
    creates the domain entity and persists it to the repository.

    Note: Stripe payment intent creation is handled by the use case,
    not by this command. This keeps the command testable and focused
    on domain logic.

    Attributes:
        _payment_repo: Repository for payment persistence.
        _appointment_repo: Repository for appointment lookups.
    """

    def __init__(
        self,
        payment_repo: PaymentRepository,
        appointment_repo: AppointmentRepository,
    ) -> None:
        """Initialize the command with required repositories.

        Args:
            payment_repo: Repository for payment persistence.
            appointment_repo: Repository for appointment lookups.
        """

        self._payment_repo = payment_repo
        self._appointment_repo = appointment_repo


    async def execute(
        self,
        request: CreatePaymentRequest,
    ) -> PaymentResponse:
        """Execute the payment creation flow.

        Steps:
            1. Verify the associated appointment exists.
            2. Create the domain entity with business rules.
            3. Persist the payment.
            4. Return the response DTO.

        Args:
            request: Validated payment creation data.

        Returns:
            The created payment as a response DTO.

        Raises:
            EntityNotFoundError: If the appointment does not exist.
        """

        logger.info(
            "Creating payment",
            extra={
                "extra_data": {
                    "appointment_id": str(request.appointment_id),
                    "amount": str(request.amount),
                    "payment_type": request.payment_type.value,
                }
            },
        )

        # Step 1: Verify the associated appointment exists
        appointment = await self._appointment_repo.get_by_id(request.appointment_id)

        if appointment is None:
            raise EntityNotFoundError(
                f"Appointment {request.appointment_id} not found"
            )

        # Step 2: Create the domain entity with business rules
        payment = Payment.create(
            appointment_id=request.appointment_id,
            amount=request.amount,
            payment_type=request.payment_type,
        )

        # Step 3: Persist the payment
        saved = await self._payment_repo.save(payment)

        logger.info(
            "Payment created successfully",
            extra={
                "extra_data": {
                    "payment_id": str(saved.id),
                    "status": saved.status.value,
                }
            },
        )

        # Step 4: Map domain entity to response DTO
        return PaymentResponse.model_validate(saved)
