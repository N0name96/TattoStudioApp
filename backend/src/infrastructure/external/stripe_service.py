"""Stripe payment service interface for the TattoStudioApp.

This module defines the protocol for Stripe payment processing.
The actual implementation will use the Stripe SDK to create
payment intents, process payments, and handle refunds.

For now, this provides the contract that the application layer
can depend on, following the Dependency Inversion Principle.
"""

from decimal import Decimal
from typing import Protocol, runtime_checkable


@runtime_checkable
class StripePaymentServiceProtocol(Protocol):
    """Interface for Stripe payment processing.

    This protocol defines the contract that any Stripe service
    implementation must satisfy. It uses Python's Protocol for
    structural subtyping, allowing easy mocking in tests.

    The actual implementation will be in a StripeService class
    that uses the Stripe Python SDK.
    """

    async def create_payment_intent(
        self,
        amount: Decimal,
        currency: str = "eur",
    ) -> dict:
        """Create a Stripe payment intent.

        Args:
            amount: The amount to charge in the specified currency.
            currency: ISO 4217 currency code, defaults to "eur".

        Returns:
            A dict containing at minimum:
                - id: The Stripe payment intent ID.
                - client_secret: The client secret for the frontend.
        """
        ...


    async def confirm_payment_intent(
        self,
        stripe_payment_id: str,
    ) -> bool:
        """Confirm a payment intent was successfully completed.

        Args:
            stripe_payment_id: The Stripe payment intent ID to verify.

        Returns:
            True if the payment was successfully completed.
        """
        ...


    async def refund_payment(
        self,
        stripe_payment_id: str,
    ) -> bool:
        """Refund a completed payment via Stripe.

        Args:
            stripe_payment_id: The Stripe payment intent ID to refund.

        Returns:
            True if the refund was successfully processed.
        """
        ...
