"""Queries init for consents."""

from application.queries.consents.get_consent_query import GetConsentQuery
from application.queries.consents.list_consents_query import ListConsentsQuery

__all__ = [
    "GetConsentQuery",
    "ListConsentsQuery",
]
