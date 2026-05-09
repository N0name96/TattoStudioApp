"""Custom error classes for the TattoStudioApp application.

This module contains the complete error hierarchy used across all layers.
Errors are organized by layer (Domain, Application, Infrastructure)
and inherit from a common BaseError class.

Hierarchy:
    BaseError
    ├── DomainError
    │   ├── EntityNotFoundError
    │   ├── BusinessRuleError
    │   └── DuplicateEntityError
    ├── ApplicationError
    │   ├── ValidationError
    │   ├── UnauthorizedError
    │   └── ForbiddenError
    └── InfrastructureError
        ├── DatabaseError
        └── ExternalServiceError
"""


class BaseError(Exception):
    """Base error class for all application errors.

    All custom errors in the application inherit from this class
    to provide a consistent error interface with code and message.

    Attributes:
        message: Human-readable error description.
        code: Machine-readable error code for API clients.
    """

    def __init__(self, message: str, code: str = "UNKNOWN_ERROR") -> None:
        """Initialize the error with a message and error code.

        Args:
            message: Human-readable error description.
            code: Machine-readable error code for clients.
        """

        self.message = message
        self.code = code

        super().__init__(message)


# =============================================================================
# Domain Errors
# =============================================================================


class DomainError(BaseError):
    """Base error for domain layer violations.

    Raised when business rules are broken or entities are not found.
    """

    pass


class EntityNotFoundError(DomainError):
    """Raised when a requested entity does not exist in the system.

    Maps to HTTP 404 Not Found.
    """

    def __init__(self, message: str = "Entity not found") -> None:
        """Initialize with a descriptive message.

        Args:
            message: Description of which entity was not found.
        """

        super().__init__(message, code="ENTITY_NOT_FOUND")


class BusinessRuleError(DomainError):
    """Raised when a business rule or invariant is violated.

    Maps to HTTP 422 Unprocessable Entity.
    """

    def __init__(self, message: str = "Business rule violated") -> None:
        """Initialize with a descriptive message.

        Args:
            message: Description of which rule was violated.
        """

        super().__init__(message, code="BUSINESS_RULE_ERROR")


class DuplicateEntityError(DomainError):
    """Raised when attempting to create an entity that already exists.

    Maps to HTTP 409 Conflict.
    """

    def __init__(self, message: str = "Entity already exists") -> None:
        """Initialize with a descriptive message.

        Args:
            message: Description of which entity already exists.
        """

        super().__init__(message, code="DUPLICATE_ENTITY")


# =============================================================================
# Application Errors
# =============================================================================


class ApplicationError(BaseError):
    """Base error for application layer violations.

    Raised when application-level operations fail,
    such as validation errors or authorization issues.
    """

    pass


class ValidationError(ApplicationError):
    """Raised when input data fails validation rules.

    Maps to HTTP 422 Unprocessable Entity.
    """

    def __init__(self, message: str = "Validation failed") -> None:
        """Initialize with a descriptive message.

        Args:
            message: Description of what validation failed.
        """

        super().__init__(message, code="VALIDATION_ERROR")


class UnauthorizedError(ApplicationError):
    """Raised when authentication is missing or invalid.

    Maps to HTTP 401 Unauthorized.
    """

    def __init__(self, message: str = "Unauthorized") -> None:
        """Initialize with a descriptive message.

        Args:
            message: Description of why auth failed.
        """

        super().__init__(message, code="UNAUTHORIZED")


class ForbiddenError(ApplicationError):
    """Raised when user lacks permission for the requested action.

    Maps to HTTP 403 Forbidden.
    """

    def __init__(self, message: str = "Forbidden") -> None:
        """Initialize with a descriptive message.

        Args:
            message: Description of what permission is missing.
        """

        super().__init__(message, code="FORBIDDEN")


# =============================================================================
# Infrastructure Errors
# =============================================================================


class InfrastructureError(BaseError):
    """Base error for infrastructure layer failures.

    Raised when external services or persistence operations fail.
    """

    pass


class DatabaseError(InfrastructureError):
    """Raised when a database operation fails.

    Maps to HTTP 500 Internal Server Error.
    """

    def __init__(self, message: str = "Database error occurred") -> None:
        """Initialize with a descriptive message.

        Args:
            message: Description of what database operation failed.
        """

        super().__init__(message, code="DATABASE_ERROR")


class ExternalServiceError(InfrastructureError):
    """Raised when an external service call fails.

    Maps to HTTP 502 Bad Gateway.

    Attributes:
        service: Name of the external service that failed.
    """

    def __init__(self, service: str, message: str = "External service error") -> None:
        """Initialize with service name and descriptive message.

        Args:
            service: Name of the external service (e.g., 'Stripe', 'SendGrid').
            message: Description of what went wrong.
        """

        self.service = service

        super().__init__(f"{service}: {message}", code="EXTERNAL_SERVICE_ERROR")
