"""API middleware package for the TattoStudioApp.

Middleware components that process HTTP requests and responses,
including error handling and authentication.
"""

from api.middleware.error_handler import register_error_handlers

__all__ = ["register_error_handlers"]
