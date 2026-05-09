"""Standardized response models for the TattoStudioApp API.

This module provides consistent response formats for all API endpoints.
Use SuccessResponse for successful operations and ErrorResponse for failures.

Usage:
    # Success response
    return SuccessResponse(data=artist, message="Artist created")

    # Error response (usually handled by global error handler)
    return ErrorResponse(error=ErrorDetail(code="NOT_FOUND", message="..."))
"""

from typing import Any, Generic, TypeVar

from pydantic import BaseModel

T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    """Standard success response wrapper for all API endpoints.

    Provides a consistent response format with success flag,
    generic data payload, and optional message.

    Attributes:
        success: Always True for successful responses.
        data: The response payload (generic type).
        message: Optional human-readable success message.
    """

    success: bool = True
    data: T
    message: str | None = None


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response wrapper for list endpoints.

    Extends the success format with pagination metadata
    to support client-side navigation through large datasets.

    Attributes:
        success: Always True for successful responses.
        data: List of items for the current page.
        total: Total number of items across all pages.
        page: Current page number (1-indexed).
        per_page: Number of items per page.
        total_pages: Total number of pages available.
    """

    success: bool = True
    data: list[T]
    total: int
    page: int
    per_page: int
    total_pages: int


class ErrorDetail(BaseModel):
    """Structured error information.

    Contains the error code, human-readable message,
    and optional additional details for debugging.

    Attributes:
        code: Machine-readable error code (e.g., "ENTITY_NOT_FOUND").
        message: Human-readable error description.
        details: Optional list of additional error details.
    """

    code: str
    message: str
    details: list[dict[str, Any]] | None = None


class ErrorResponse(BaseModel):
    """Standard error response wrapper for all API endpoints.

    Provides a consistent error format with success flag
    and structured error details.

    Attributes:
        success: Always False for error responses.
        error: Structured error information.
    """

    success: bool = False
    error: ErrorDetail
