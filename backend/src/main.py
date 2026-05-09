"""FastAPI application entry point.

This module creates and configures the FastAPI application instance,
registers routers, and sets up middleware.
"""

import sys
from pathlib import Path

# Add src directory to Python path for absolute imports
sys.path.insert(0, str(Path(__file__).parent))


import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.middleware.error_handler import register_error_handlers
from api.v1.endpoints.appointment_handler import router as appointment_router
from api.v1.endpoints.artist_handler import router as artist_router
from api.v1.endpoints.auth_handler import router as auth_router
from api.v1.endpoints.cash_handler import router as cash_router
from api.v1.endpoints.client_handler import router as client_router
from api.v1.endpoints.consent_handler import router as consent_router
from api.v1.endpoints.payment_handler import router as payment_router
from api.v1.endpoints.product_handler import router as product_router
from api.v1.endpoints.notification_handler import router as notification_router
from api.v1.endpoints.metrics_handler import router as metrics_router
from core.config import settings
from core.logging import setup_logging

# Initialize structured logging
setup_logging(log_level=settings.LOG_LEVEL)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler.

    Runs on startup and shutdown events.
    Used for initializing connections and cleanup.
    """

    logger.info("Starting TattoStudioApp", extra={"extra_data": {"version": "0.1.0"}})
    yield
    logger.info("Shutting down TattoStudioApp")


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    description="API for managing tattoo studio operations",
    version="0.1.0",
    lifespan=lifespan,
)

# Register global error handlers
register_error_handlers(app)

# Register routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(appointment_router, prefix="/api/v1")
app.include_router(artist_router, prefix="/api/v1")
app.include_router(cash_router, prefix="/api/v1")
app.include_router(client_router, prefix="/api/v1")
app.include_router(payment_router, prefix="/api/v1")
app.include_router(consent_router, prefix="/api/v1")
app.include_router(product_router, prefix="/api/v1")
app.include_router(notification_router, prefix="/api/v1")
app.include_router(metrics_router, prefix="/api/v1")


@app.get("/")
async def root():
    """Health check endpoint."""

    return {"status": "ok", "service": settings.APP_NAME}


@app.get("/health")
async def health():
    """Detailed health check endpoint."""

    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": "0.1.0",
    }
