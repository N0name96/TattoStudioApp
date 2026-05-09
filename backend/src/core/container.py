"""Dependency injection container for the TattoStudioApp.

This module provides a simple singleton container for managing
service instances and their dependencies.

Usage:
    from core.container import container

    user_repo = container.user_repository
"""

import logging

from domain.repositories.appointment_repository import AppointmentRepository
from domain.repositories.artist_repository import ArtistRepository
from domain.repositories.cash_repository import CashRepository
from domain.repositories.client_repository import ClientRepository
from domain.repositories.consent_repository import ConsentRepository
from domain.repositories.notification_repository import NotificationRepository
from domain.repositories.payment_repository import PaymentRepository
from domain.repositories.product_repository import ProductRepository
from domain.repositories.user_repository import UserRepository
from infrastructure.security.security_service import SecurityService

logger = logging.getLogger(__name__)


class Container:
    """Simple dependency injection container.

    Manages singleton instances of repositories and services.
    Lazy initialization ensures instances are created only when needed.

    Attributes:
        _user_repository: Singleton user repository instance.
        _appointment_repository: Singleton appointment repository instance.
        _artist_repository: Singleton artist repository instance.
        _cash_repository: Singleton cash repository instance.
        _client_repository: Singleton client repository instance.
        _payment_repository: Singleton payment repository instance.
        _consent_repository: Singleton consent repository instance.
        _product_repository: Singleton product repository instance.
        _notification_repository: Singleton notification repository instance.
        _security_service: Singleton security service instance.
    """

    def __init__(self) -> None:
        """Initialize the container with empty instances."""

        self._user_repository: UserRepository | None = None
        self._appointment_repository: AppointmentRepository | None = None
        self._artist_repository: ArtistRepository | None = None
        self._cash_repository: CashRepository | None = None
        self._client_repository: ClientRepository | None = None
        self._payment_repository: PaymentRepository | None = None
        self._consent_repository: ConsentRepository | None = None
        self._product_repository: ProductRepository | None = None
        self._notification_repository: NotificationRepository | None = None
        self._security_service: SecurityService | None = None

    @property
    def user_repository(self) -> UserRepository:
        """Get the singleton user repository instance.

        Returns:
            A UserRepository implementation.
        """

        if self._user_repository is None:
            from infrastructure.persistence.in_memory.user_repository import (
                InMemoryUserRepository,
            )

            self._user_repository = InMemoryUserRepository()
            logger.info("UserRepository initialized")

        return self._user_repository

    @property
    def appointment_repository(self) -> AppointmentRepository:
        """Get the singleton appointment repository instance.

        Returns:
            An AppointmentRepository implementation.
        """

        if self._appointment_repository is None:
            from infrastructure.persistence.in_memory.appointment_repository import (
                InMemoryAppointmentRepository,
            )

            self._appointment_repository = InMemoryAppointmentRepository()
            logger.info("AppointmentRepository initialized")

        return self._appointment_repository

    @property
    def artist_repository(self) -> ArtistRepository:
        """Get the singleton artist repository instance.

        Returns:
            An ArtistRepository implementation.
        """

        if self._artist_repository is None:
            from infrastructure.persistence.in_memory.artist_repository import (
                InMemoryArtistRepository,
            )

            self._artist_repository = InMemoryArtistRepository()
            logger.info("ArtistRepository initialized")

        return self._artist_repository

    @property
    def cash_repository(self) -> CashRepository:
        """Get the singleton cash repository instance.

        Returns:
            A CashRepository implementation.
        """

        if self._cash_repository is None:
            from infrastructure.persistence.in_memory.cash_repository import (
                InMemoryCashRepository,
            )

            self._cash_repository = InMemoryCashRepository()
            logger.info("CashRepository initialized")

        return self._cash_repository

    @property
    def client_repository(self) -> ClientRepository:
        """Get the singleton client repository instance.

        Returns:
            A ClientRepository implementation.
        """

        if self._client_repository is None:
            from infrastructure.persistence.in_memory.client_repository import (
                InMemoryClientRepository,
            )

            self._client_repository = InMemoryClientRepository()
            logger.info("ClientRepository initialized")

        return self._client_repository

    @property
    def payment_repository(self) -> PaymentRepository:
        """Get the singleton payment repository instance.

        Returns:
            A PaymentRepository implementation.
        """

        if self._payment_repository is None:
            from infrastructure.persistence.in_memory.payment_repository import (
                InMemoryPaymentRepository,
            )

            self._payment_repository = InMemoryPaymentRepository()
            logger.info("PaymentRepository initialized")

        return self._payment_repository

    @property
    def consent_repository(self) -> ConsentRepository:
        """Get the singleton consent repository instance.

        Returns:
            A ConsentRepository implementation.
        """

        if self._consent_repository is None:
            from infrastructure.persistence.in_memory.consent_repository import (
                InMemoryConsentRepository,
            )

            self._consent_repository = InMemoryConsentRepository()
            logger.info("ConsentRepository initialized")

        return self._consent_repository

    @property
    def product_repository(self) -> ProductRepository:
        """Get the singleton product repository instance."""

        if self._product_repository is None:
            from infrastructure.persistence.in_memory.product_repository import (
                InMemoryProductRepository,
            )

            self._product_repository = InMemoryProductRepository()
            logger.info("ProductRepository initialized")

        return self._product_repository

    @property
    def notification_repository(self) -> NotificationRepository:
        if self._notification_repository is None:
            from infrastructure.persistence.in_memory.notification_repository import (
                InMemoryNotificationRepository,
            )
            self._notification_repository = InMemoryNotificationRepository()
            logger.info("NotificationRepository initialized")
        return self._notification_repository

    @property
    def security_service(self) -> SecurityService:
        """Get the singleton security service instance.

        Returns:
            A SecurityService instance.
        """

        if self._security_service is None:
            self._security_service = SecurityService()
            logger.info("SecurityService initialized")

        return self._security_service


# Global container instance
container = Container()
