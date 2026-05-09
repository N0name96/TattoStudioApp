"""Request DTOs for consents."""

from application.dto.requests.consents.create_consent_request import (
    CreateConsentRequest,
)
from application.dto.requests.consents.sign_consent_request import (
    SignConsentRequest,
)

__all__ = [
    "CreateConsentRequest",
    "SignConsentRequest",
]
