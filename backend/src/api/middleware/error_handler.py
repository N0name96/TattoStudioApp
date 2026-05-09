"""Global error handler middleware for the TattoStudioApp API.

Registers exception handlers on the FastAPI application that catch
all custom application errors and unhandled exceptions, converting
them into consistent ErrorResponse JSON payloads.

Error mapping:
    - EntityNotFoundError → 404
    - DuplicateEntityError → 409
    - BusinessRuleError, ValidationError → 422
    - UnauthorizedError → 401
    - ForbiddenError → 403
    - ExternalServiceError → 502
    - DomainError, ApplicationError, InfrastructureError → 400
    - Unhandled exceptions → 500 (generic, no internals exposed)
"""

import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from core.errors import (
    ApplicationError,
    BaseError,
    BusinessRuleError,
    DomainError,
    DuplicateEntityError,
    EntityNotFoundError,
    ExternalServiceError,
    ForbiddenError,
    InfrastructureError,
    UnauthorizedError,
    ValidationError,
)
from core.responses import ErrorDetail, ErrorResponse

logger = logging.getLogger(__name__)


def register_error_handlers(app: FastAPI) -> None:
    """Register global exception handlers on the FastAPI application.

    This function configures centralized error handling that catches
    all exceptions and converts them into consistent API responses.

    Args:
        app: The FastAPI application instance.
    """

    @app.exception_handler(BaseError)
    async def handle_base_error(request: Request, exc: BaseError) -> JSONResponse:
        """Handle all custom application errors.

        Maps domain, application, and infrastructure errors to
        appropriate HTTP status codes and structured responses.

        Args:
            request: The HTTP request that caused the error.
            exc: The custom exception that was raised.

        Returns:
            A JSON response with structured error details.
        """

        # Determine HTTP status code based on error type
        status_code = 500

        if isinstance(exc, EntityNotFoundError):
            status_code = 404
        elif isinstance(exc, DuplicateEntityError):
            status_code = 409
        elif isinstance(exc, (BusinessRuleError, ValidationError)):
            status_code = 422
        elif isinstance(exc, UnauthorizedError):
            status_code = 401
        elif isinstance(exc, ForbiddenError):
            status_code = 403
        elif isinstance(exc, ExternalServiceError):
            status_code = 502
        elif isinstance(exc, (DomainError, ApplicationError, InfrastructureError)):
            status_code = 400

        # Log the error
        logger.warning(
            "Application error",
            extra={
                "extra_data": {
                    "path": request.url.path,
                    "method": request.method,
                    "status_code": status_code,
                    "error_code": exc.code,
                    "error_message": exc.message,
                }
            },
        )

        # Build structured error response
        response = ErrorResponse(
            error=ErrorDetail(
                code=exc.code,
                message=exc.message,
            )
        )

        return JSONResponse(
            status_code=status_code,
            content=response.model_dump(),
        )


    @app.exception_handler(Exception)
    async def handle_unhandled_exception(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """Global handler for unhandled exceptions.

        Catches unexpected errors, logs them with full context,
        and returns a generic 500 error to the client.
        Never exposes internal details to the client.

        Args:
            request: The HTTP request that caused the error.
            exc: The unexpected exception.

        Returns:
            A JSON response with a generic 500 error.
        """

        logger.error(
            "Unhandled exception",
            extra={
                "extra_data": {
                    "path": request.url.path,
                    "method": request.method,
                    "error_type": type(exc).__name__,
                    "error_message": str(exc),
                }
            },
            exc_info=True,
        )

        response = ErrorResponse(
            error=ErrorDetail(
                code="INTERNAL_SERVER_ERROR",
                message="An unexpected error occurred. Please try again later.",
            )
        )

        return JSONResponse(
            status_code=500,
            content=response.model_dump(),
        )
