"""Commands init for consents."""

from application.commands.consents.create_consent_command import (
    CreateConsentCommand,
)
from application.commands.consents.revoke_consent_command import (
    RevokeConsentCommand,
)
from application.commands.consents.sign_consent_command import (
    SignConsentCommand,
)

__all__ = [
    "CreateConsentCommand",
    "RevokeConsentCommand",
    "SignConsentCommand",
]
