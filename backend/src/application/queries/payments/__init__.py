"""Queries init for payments."""

from application.queries.payments.get_payment_query import GetPaymentQuery
from application.queries.payments.list_payments_query import ListPaymentsQuery

__all__ = [
    "GetPaymentQuery",
    "ListPaymentsQuery",
]
