"""Structured logging configuration for the TattoStudioApp.

This module provides JSON-formatted logging with consistent fields
for easy parsing by log aggregation tools (ELK, Datadog, etc.)

Usage:
    from core.logging import setup_logging

    setup_logging(log_level="INFO")
"""

import json
import logging
import sys
from datetime import UTC, datetime
from typing import Any


class StructuredFormatter(logging.Formatter):
    """Custom formatter that outputs structured JSON logs.

    Produces machine-readable logs with consistent fields
    for all loggers in the application.

    Output format:
        {
            "timestamp": "2026-05-08T14:30:00.000Z",
            "level": "ERROR",
            "logger": "api.endpoints.appointment_handler",
            "message": "Failed to create appointment",
            "data": { ... }
        }
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record as a JSON string.

        Args:
            record: The log record to format.

        Returns:
            A JSON string with structured log data.
        """

        log_data: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        # Add extra fields if present
        if hasattr(record, "extra_data"):
            log_data["data"] = record.extra_data

        # Add exception info if present
        if record.exc_info and record.exc_info[0] is not None:
            log_data["exception"] = {
                "type": record.exc_info[0].__name__,
                "message": str(record.exc_info[1]),
                "traceback": self.formatException(record.exc_info),
            }

        return json.dumps(log_data)


def setup_logging(log_level: str = "INFO") -> None:
    """Configure structured logging for the application.

    Sets up JSON-formatted logs with consistent fields
    for all loggers in the application.

    Args:
        log_level: The minimum log level to output (DEBUG, INFO, WARNING, ERROR).
    """

    # Create structured formatter
    formatter = StructuredFormatter()

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))

    # Remove existing handlers to avoid duplicates
    root_logger.handlers.clear()

    # Console handler with structured output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Suppress noisy library loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("supabase").setLevel(logging.WARNING)
    logging.getLogger("urllib3").setLevel(logging.WARNING)
