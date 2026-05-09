"""Request DTO for refunding a payment."""

from pydantic import BaseModel


class RefundPaymentRequest(BaseModel):
    """Request DTO for refunding a payment.

    This is intentionally empty as the payment ID comes from the URL path.
    It exists for API consistency and can be extended with reason field in the future.
    """

    pass
