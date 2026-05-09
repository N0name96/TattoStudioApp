"""Use case for payment operations in the TattoStudioApp.

This module provides a high-level interface for payment operations,
orchestrating commands, queries and the Stripe service.
"""

import logging
from uuid import UUID

from application.commands.payments.create_payment_command import (
    CreatePaymentCommand,
)
from application.commands.payments.refund_payment_command import (
    RefundPaymentCommand,
)
from application.dto.requests.payments.create_payment_request import (
    CreatePaymentRequest,
)
from application.dto.responses.payments.payment_response import (
    PaymentResponse,
)
from application.queries.payments.get_payment_query import (
    GetPaymentQuery,
)
from application.queries.payments.list_payments_query import (
    ListPaymentsQuery,
)
from domain.enums.payment_status import PaymentStatus
from domain.repositories.appointment_repository import AppointmentRepository
from domain.repositories.payment_repository import PaymentRepository

logger = logging.getLogger(__name__)


class PaymentUseCase:
    """Use case for payment operations.

    Orchestrates commands, queries and the Stripe service
    for the payments module. Provides a single entry point
    for the API layer.

    Attributes:
        _payment_repo: Repository for payment persistence.
        _appointment_repo: Repository for appointment lookups.
        _create_command: Command for creating payments.
        _refund_command: Command for refunding payments.
        _get_query: Query for retrieving a single payment.
        _list_query: Query for listing payments.
    """

    def __init__(
        self,
        payment_repo: PaymentRepository,
        appointment_repo: AppointmentRepository,
    ) -> None:
        """Initialize the use case with required repositories.

        Args:
            payment_repo: Repository for payment persistence.
            appointment_repo: Repository for appointment lookups.
        """

        self._payment_repo = payment_repo
        self._appointment_repo = appointment_repo
        self._create_command = CreatePaymentCommand(
            payment_repo, appointment_repo
        )
        self._refund_command = RefundPaymentCommand(payment_repo)
        self._get_query = GetPaymentQuery(payment_repo)
        self._list_query = ListPaymentsQuery(payment_repo)


    async def create_payment(
        self,
        request: CreatePaymentRequest,
    ) -> PaymentResponse:
        """Create a new payment for an appointment.

        Args:
            request: Validated payment creation data.

        Returns:
            The created payment as a response DTO.
        """

        return await self._create_command.execute(request)


    async def get_payment(self, payment_id: UUID) -> PaymentResponse:
        """Retrieve a single payment by ID.

        Args:
            payment_id: UUID of the payment to retrieve.

        Returns:
            The payment as a response DTO.
        """

        return await self._get_query.execute(payment_id)


    async def list_payments(
        self,
        appointment_id: UUID | None = None,
        status: PaymentStatus | None = None,
    ) -> list[PaymentResponse]:
        """List payments with optional filters.

        Args:
            appointment_id: Optional filter by appointment UUID.
            status: Optional filter by payment status.

        Returns:
            A list of payment response DTOs.
        """

        return await self._list_query.execute(
            appointment_id=appointment_id,
            status=status,
        )


    async def refund_payment(self, payment_id: UUID) -> PaymentResponse:
        """Refund a completed payment.

        Note: In the full implementation, this would call the Stripe
        service to process the refund before updating the entity.

        Args:
            payment_id: UUID of the payment to refund.

        Returns:
            The updated payment as a response DTO.
        """

        return await self._refund_command.execute(payment_id)
