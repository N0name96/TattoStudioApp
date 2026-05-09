# TattoStudioApp - Arquitectura Técnica

## 1. Visión General de la Arquitectura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Web     │    │  React Native   │    │   Admin Panel   │
│   (Cliente)     │    │  (Expo/Móvil)   │    │   (Web Admin)   │
└────────┬────────┘    └────────┬────────┘    └────────┬────────┘
         │                      │                      │
         └──────────────────────┼──────────────────────┘
                                │
                         ┌──────▼──────┐
                         │   FastAPI    │
                         │   API Layer  │
                         └──────┬──────┘
                                │
                    ┌───────────▼───────────┐
                    │    Application Layer   │
                    │   (Use Cases / CQRS)  │
                    └───────────┬───────────┘
                                │
                 ┌──────────────┼──────────────┐
                 │                             │
          ┌──────▼──────┐              ┌───────▼───────┐
          │ Domain Layer │              │Infrastructure │
          │ (Entities,   │              │  Layer        │
          │  Protocols)  │              │ (Supabase,    │
          └──────────────┘              │  External)    │
                                        └───────────────┘
```

## 2. Principios de Diseño

### SOLID

| Principio | Aplicación |
|-----------|-----------|
| **S** - Single Responsibility | Cada clase/módulo tiene una única razón para cambiar |
| **O** - Open/Closed | Abierto a extensión, cerrado a modificación (usar Protocols/interfaces) |
| **L** - Liskov Substitution | Las implementaciones deben ser sustituibles por sus Protocolos |
| **I** - Interface Segregation | Protocolos específicos y pequeños, no genéricos |
| **D** - Dependency Inversion | Las capas superiores dependen de abstracciones (Protocolos), no de implementaciones |

### Clean Architecture

Las dependencias van siempre hacia adentro: **API → APPLICATION → DOMAIN ← INFRASTRUCTURE**

- **DOMAIN** no depende de nada (capa más interna)
- **APPLICATION** depende solo de DOMAIN
- **INFRASTRUCTURE** implementa los Protocolos de DOMAIN
- **API** orquesta a través de APPLICATION

### CQRS (Command Query Responsibility Segregation)

- **Commands**: Operaciones de escritura (Create, Update, Delete) → Modifican estado
- **Queries**: Operaciones de lectura (Get, List, Search) → Solo leen estado
- Cada uno con su propio handler y DTO de entrada/salida

## 3. Stack Tecnológico

### Frontend Web (React)
- **Framework**: React 18+ con TypeScript
- **Routing**: React Router v6
- **Estado**: Zustand
- **UI**: Tailwind CSS + shadcn/ui
- **HTTP Client**: TanStack Query + Axios
- **Build**: Vite

### Frontend Móvil (React Native)
- **Framework**: React Native con Expo SDK 51+
- **Navegación**: Expo Router
- **Estado**: Zustand (compartido con web)
- **UI**: NativeWind (Tailwind para RN)
- **Notificaciones**: Expo Notifications
- **Build**: EAS Build

### Backend (FastAPI)
- **Framework**: FastAPI (Python 3.11+)
- **Validación**: Pydantic v2 (DTOs separados de handlers)
- **Auth**: JWT (python-jose) + passlib (bcrypt)
- **Tareas asíncronas**: Celery + Redis
- **Documentación**: OpenAPI automático (Swagger)

### Base de Datos
- **Principal**: Supabase (PostgreSQL managed)
- **Auth**: Supabase Auth (opcional, o JWT propio)
- **Storage**: Supabase Storage (imágenes, consentimientos)
- **Realtime**: Supabase Realtime (notificaciones in-app)
- **Cache**: Redis 7

### Infraestructura
- **Containerización**: Docker + Docker Compose
- **CI/CD**: GitHub Actions
- **Hosting Backend**: Railway / Render / VPS
- **Hosting Web**: Vercel / Netlify
- **Móvil**: EAS (Expo Application Services)

## 4. Estructura de Directorios (Backend - Clean Architecture)

```
backend/
├── src/
│   ├── api/                              # CAPA API (Endpoints, Handlers)
│   │   ├── v1/
│   │   │   ├── endpoints/
│   │   │   │   ├── auth_handler.py       # Handler de autenticación
│   │   │   │   ├── artist_handler.py     # Handler de artistas
│   │   │   │   ├── appointment_handler.py# Handler de citas
│   │   │   │   ├── payment_handler.py    # Handler de pagos
│   │   │   │   ├── consent_handler.py    # Handler de consentimientos
│   │   │   │   ├── cash_handler.py       # Handler de caja/productos
│   │   │   │   ├── metrics_handler.py    # Handler de métricas
│   │   │   │   └── notification_handler.py
│   │   │   └── router.py
│   │   ├── deps.py                       # Dependencias (DI container)
│   │   └── middleware/
│   │       ├── auth_middleware.py
│   │       └── error_middleware.py
│   │
│   ├── application/                      # CAPA APPLICATION (Use Cases / CQRS)
│   │   ├── commands/                     # Commands (escritura)
│   │   │   ├── create_appointment_command.py
│   │   │   ├── sign_consent_command.py
│   │   │   ├── process_payment_command.py
│   │   │   ├── create_artist_command.py
│   │   │   └── ...
│   │   ├── queries/                      # Queries (lectura)
│   │   │   ├── get_artist_query.py
│   │   │   ├── list_appointments_query.py
│   │   │   ├── get_metrics_query.py
│   │   │   └── ...
│   │   ├── use_cases/                    # Use Cases (orquestan commands/queries)
│   │   │   ├── appointment_use_case.py
│   │   │   ├── consent_use_case.py
│   │   │   ├── payment_use_case.py
│   │   │   └── ...
│   │   └── dto/                          # DTOs Pydantic (SEPARADOS de handlers)
│   │       ├── requests/
│   │       │   ├── create_appointment_request.py
│   │       │   ├── sign_consent_request.py
│   │       │   └── ...
│   │       └── responses/
│   │           ├── appointment_response.py
│   │           ├── artist_response.py
│   │           └── ...
│   │
│   ├── domain/                           # CAPA DOMAIN (Entidades, Interfaces)
│   │   ├── entities/
│   │   │   ├── user_entity.py
│   │   │   ├── artist_entity.py
│   │   │   ├── appointment_entity.py
│   │   │   ├── payment_entity.py
│   │   │   ├── consent_entity.py
│   │   │   ├── product_entity.py
│   │   │   └── ...
│   │   ├── value_objects/
│   │   │   ├── email_vo.py
│   │   │   ├── money_vo.py
│   │   │   ├── date_range_vo.py
│   │   │   └── ...
│   │   ├── enums/
│   │   │   ├── user_role.py
│   │   │   ├── appointment_status.py
│   │   │   ├── payment_status.py
│   │   │   ├── service_type.py
│   │   │   └── ...
│   │   ├── repositories/                 # Interfaces (Protocols, NO ABC)
│   │   │   ├── artist_repository.py
│   │   │   ├── appointment_repository.py
│   │   │   ├── payment_repository.py
│   │   │   ├── consent_repository.py
│   │   │   ├── client_repository.py
│   │   │   ├── product_repository.py
│   │   │   └── ...
│   │   └── services/                     # Servicios de dominio puros
│   │       ├── commission_calculator.py
│   │       └── ...
│   │
│   ├── infrastructure/                   # CAPA INFRASTRUCTURE (Implementaciones)
│   │   ├── persistence/
│   │   │   ├── supabase/
│   │   │   │   ├── client.py             # Cliente Supabase
│   │   │   │   ├── artist_repository.py  # Implementación concreta
│   │   │   │   ├── appointment_repository.py
│   │   │   │   ├── payment_repository.py
│   │   │   │   ├── consent_repository.py
│   │   │   │   ├── client_repository.py
│   │   │   │   ├── product_repository.py
│   │   │   │   └── mappers.py            # Mappers DB Entity ↔ Domain Entity
│   │   │   └── models/                   # Modelos de datos Supabase (si se usan)
│   │   │       └── supabase_models.py
│   │   ├── external/
│   │   │   ├── google_calendar_service.py
│   │   │   ├── email_service.py
│   │   │   ├── stripe_service.py
│   │   │   └── storage_service.py
│   │   └── tasks/
│   │       ├── notification_tasks.py     # Tareas Celery
│   │       └── reminder_tasks.py
│   │
│   └── core/                             # CAPA CORE (Errores, Respuestas, Config)
│       ├── errors/
│       │   ├── base_error.py             # BaseError
│       │   ├── domain_errors.py          # EntityNotFoundError, BusinessRuleError
│       │   ├── application_errors.py     # UseCaseError, ValidationError
│       │   └── infrastructure_errors.py  # DatabaseError, ExternalServiceError
│       ├── responses/
│       │   ├── success_response.py       # SuccessResponse[T]
│       │   ├── error_response.py         # ErrorResponse
│       │   └── pagination_response.py    # PaginatedResponse[T]
│       ├── config.py                     # Settings (pydantic-settings)
│       ├── security.py                   # JWT, hashing
│       ├── container.py                  # DI Container
│       └── logging.py
│
├── tests/
│   ├── unit/
│   │   ├── domain/
│   │   │   ├── test_artist_entity.py
│   │   │   ├── test_appointment_entity.py
│   │   │   └── test_commission_calculator.py
│   │   ├── application/
│   │   │   ├── commands/
│   │   │   │   ├── test_create_appointment_command.py
│   │   │   │   └── test_sign_consent_command.py
│   │   │   ├── queries/
│   │   │   │   ├── test_get_artist_query.py
│   │   │   │   └── test_list_appointments_query.py
│   │   │   └── use_cases/
│   │   │       └── test_appointment_use_case.py
│   │   └── core/
│   │       ├── test_errors.py
│   │       └── test_responses.py
│   ├── integration/
│   │   ├── api/
│   │   │   └── test_artist_handler.py
│   │   └── infrastructure/
│   │       └── test_supabase_repository.py
│   └── conftest.py                       # Fixtures compartidos
│
├── alembic/                              # Migraciones (si se usan)
├── requirements.txt
├── Dockerfile
├── pyproject.toml
└── alembic.ini
```

## 5. Ejemplos de Implementación por Capa

### 5.1 Domain Layer - Entity (con Protocols)

```python
# domain/entities/artist_entity.py
from dataclasses import dataclass
from uuid import UUID


@dataclass
class Artist:
    """Represents an artist in the tattoo studio.

    This entity contains the core business logic for an artist,
    including activation/deactivation and rating management.
    """

    id: UUID
    user_id: UUID
    bio: str
    specialities: list[str]
    instagram: str | None
    rating_avg: float
    is_active: bool


    def deactivate(self) -> None:
        """Deactivate the artist, preventing new appointments.

        Raises:
            BusinessRuleError: If the artist is already inactive.
        """

        if not self.is_active:
            raise BusinessRuleError("Artist is already inactive")

        self.is_active = False


    def update_rating(self, new_rating: float) -> None:
        """Update the artist's average rating with a new review.

        Args:
            new_rating: The new rating value (1-5).
        """

        self.rating_avg = (self.rating_avg + new_rating) / 2
```

```python
# domain/repositories/artist_repository.py
from typing import Protocol, runtime_checkable
from uuid import UUID
from domain.entities.artist_entity import Artist


@runtime_checkable
class ArtistRepository(Protocol):
    """Interface for Artist persistence.

    This protocol defines the contract that any artist repository
    implementation must satisfy. Implemented in Infrastructure layer.
    """

    async def get_by_id(self, artist_id: UUID) -> Artist | None:
        """Retrieve an artist by their unique identifier."""
        ...

    async def get_all(self, active_only: bool = True) -> list[Artist]:
        """Retrieve all artists, optionally filtering by active status."""
        ...

    async def save(self, artist: Artist) -> Artist:
        """Persist an artist entity (create or update)."""
        ...

    async def delete(self, artist_id: UUID) -> None:
        """Remove an artist by their unique identifier."""
        ...

    async def find_by_user_id(self, user_id: UUID) -> Artist | None:
        """Find an artist associated with a given user account."""
        ...
```

```python
# domain/value_objects/money_vo.py
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Money:
    """Value object representing a monetary amount with currency.

    Immutable by design. All operations return new instances
    to prevent accidental mutation of financial data.
    """

    amount: Decimal
    currency: str = "EUR"


    def __post_init__(self) -> None:
        """Validate that the amount is not negative."""

        if self.amount < 0:
            raise ValueError("Amount cannot be negative")


    def add(self, other: "Money") -> "Money":
        """Add two Money amounts of the same currency.

        Args:
            other: Another Money instance to add.

        Returns:
            A new Money instance with the summed amount.

        Raises:
            ValueError: If the currencies do not match.
        """

        if self.currency != other.currency:
            raise ValueError("Cannot add different currencies")

        return Money(amount=self.amount + other.amount, currency=self.currency)
```

```python
# domain/enums/appointment_status.py
from enum import Enum


class AppointmentStatus(str, Enum):
    """Represents the possible states of an appointment.

    Uses str mixin for easy JSON serialization.
    """

    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"
```

### 5.2 Application Layer - CQRS (Commands + Queries + DTOs)

```python
# application/dto/requests/create_appointment_request.py
from pydantic import BaseModel, Field
from uuid import UUID
from datetime import date, time
from domain.enums.service_type import ServiceType


class CreateAppointmentRequest(BaseModel):
    """Request DTO for creating a new appointment.

    Contains all the data needed to schedule an appointment
    between a client and an artist.
    """

    artist_id: UUID
    service_type: ServiceType
    date: date
    start_time: time
    notes: str | None = None
```

```python
# application/dto/responses/appointment_response.py
from pydantic import BaseModel
from uuid import UUID
from datetime import date, time, datetime
from domain.enums.appointment_status import AppointmentStatus
from domain.enums.service_type import ServiceType


class AppointmentResponse(BaseModel):
    """Response DTO for appointment data.

    Used to return appointment information to the API layer.
    Maps from domain entity to a serializable format.
    """

    id: UUID
    client_id: UUID
    artist_id: UUID
    service_type: ServiceType
    date: date
    start_time: time
    end_time: time
    status: AppointmentStatus
    notes: str | None
    total_price: float
    created_at: datetime

    class Config:
        from_attributes = True
```

```python
# application/commands/create_appointment_command.py
from uuid import UUID
from application.dto.requests.create_appointment_request import CreateAppointmentRequest
from application.dto.responses.appointment_response import AppointmentResponse
from domain.repositories.appointment_repository import AppointmentRepository
from domain.repositories.artist_repository import ArtistRepository
from domain.entities.appointment_entity import Appointment
from core.errors.domain_errors import EntityNotFoundError, BusinessRuleError


class CreateAppointmentCommand:
    """Command to create a new appointment in the system.

    This command validates the request, checks artist availability,
    creates the domain entity and persists it to the repository.
    """

    def __init__(
        self,
        appointment_repo: AppointmentRepository,
        artist_repo: ArtistRepository,
    ) -> None:
        """Initialize the command with required repositories.

        Args:
            appointment_repo: Repository for appointment persistence.
            artist_repo: Repository for artist lookups.
        """

        self._appointment_repo = appointment_repo
        self._artist_repo = artist_repo


    async def execute(
        self,
        client_id: UUID,
        request: CreateAppointmentRequest,
    ) -> AppointmentResponse:
        """Execute the appointment creation flow.

        Steps:
            1. Verify the artist exists.
            2. Check the artist is available at the requested time.
            3. Create the domain entity.
            4. Persist and return the result.

        Raises:
            EntityNotFoundError: If the artist does not exist.
            BusinessRuleError: If the artist is not available.
        """

        # Step 1: Verify the artist exists
        artist = await self._artist_repo.get_by_id(request.artist_id)

        if artist is None:
            raise EntityNotFoundError(f"Artist {request.artist_id} not found")

        # Step 2: Check availability for the requested slot
        existing = await self._appointment_repo.find_by_artist_and_date(
            artist_id=request.artist_id,
            date=request.date,
            start_time=request.start_time,
        )

        if existing is not None:
            raise BusinessRuleError("Artist is not available at this time")

        # Step 3: Create the domain entity with business rules applied
        appointment = Appointment.create(
            client_id=client_id,
            artist_id=request.artist_id,
            service_type=request.service_type,
            date=request.date,
            start_time=request.start_time,
            notes=request.notes,
        )

        # Step 4: Persist the appointment
        saved = await self._appointment_repo.save(appointment)

        # Map domain entity to response DTO
        return AppointmentResponse.model_validate(saved)
```

```python
# application/queries/get_artist_query.py
from uuid import UUID
from application.dto.responses.artist_response import ArtistResponse
from domain.repositories.artist_repository import ArtistRepository
from core.errors.domain_errors import EntityNotFoundError


class GetArtistQuery:
    """Query to retrieve a single artist by ID.

    This query handles the read operation for artist data,
    mapping from domain entity to response DTO.
    """

    def __init__(self, artist_repo: ArtistRepository) -> None:
        """Initialize the query with the artist repository.

        Args:
            artist_repo: Repository for artist lookups.
        """

        self._artist_repo = artist_repo


    async def execute(self, artist_id: UUID) -> ArtistResponse:
        """Execute the artist retrieval.

        Args:
            artist_id: The unique identifier of the artist.

        Returns:
            The artist data as a response DTO.

        Raises:
            EntityNotFoundError: If the artist does not exist.
        """

        artist = await self._artist_repo.get_by_id(artist_id)

        if artist is None:
            raise EntityNotFoundError(f"Artist {artist_id} not found")

        return ArtistResponse.model_validate(artist)
```

### 5.3 Infrastructure Layer - Supabase Implementation

```python
# infrastructure/persistence/supabase/client.py
from supabase import create_client, AsyncClient
from core.config import settings


class SupabaseClient:
    """Singleton client for Supabase database access.

    Manages the connection lifecycle and provides a single
    point of access for all Supabase operations.
    """

    _instance: AsyncClient | None = None


    @classmethod
    async def get_client(cls) -> AsyncClient:
        """Get or create the Supabase client instance.

        Returns:
            The configured async Supabase client.
        """

        if cls._instance is None:
            cls._instance = create_client(
                supabase_url=settings.SUPABASE_URL,
                supabase_key=settings.SUPABASE_KEY,
            )

        return cls._instance
```

```python
# infrastructure/persistence/supabase/artist_repository.py
from uuid import UUID
from domain.entities.artist_entity import Artist
from domain.repositories.artist_repository import ArtistRepository as ArtistRepositoryProtocol
from infrastructure.persistence.supabase.client import SupabaseClient
from infrastructure.persistence.supabase.mappers import map_to_artist, map_to_artist_dict


class SupabaseArtistRepository:
    """Implements ArtistRepository Protocol using Supabase.

    This class provides the concrete persistence layer for Artist entities,
    translating domain operations into Supabase queries.
    """

    TABLE = "artists"


    async def get_by_id(self, artist_id: UUID) -> Artist | None:
        """Retrieve an artist by their unique ID.

        Args:
            artist_id: The UUID of the artist to find.

        Returns:
            The Artist entity if found, None otherwise.
        """

        client = await SupabaseClient.get_client()

        response = (
            client.table(self.TABLE)
            .select("*")
            .eq("id", str(artist_id))
            .execute()
        )

        if not response.data:
            return None

        return map_to_artist(response.data[0])


    async def get_all(self, active_only: bool = True) -> list[Artist]:
        """Retrieve all artists from the database.

        Args:
            active_only: If True, only return active artists.

        Returns:
            A list of Artist entities.
        """

        client = await SupabaseClient.get_client()
        query = client.table(self.TABLE).select("*")

        if active_only:
            query = query.eq("is_active", True)

        response = query.execute()

        return [map_to_artist(row) for row in response.data]


    async def save(self, artist: Artist) -> Artist:
        """Persist an artist entity (create or update).

        Uses upsert to handle both creation and updates.

        Args:
            artist: The Artist entity to persist.

        Returns:
            The persisted Artist entity with any server-generated fields.
        """

        client = await SupabaseClient.get_client()
        data = map_to_artist_dict(artist)

        response = (
            client.table(self.TABLE)
            .upsert(data)
            .execute()
        )

        return map_to_artist(response.data[0])


    async def delete(self, artist_id: UUID) -> None:
        """Remove an artist by their unique ID.

        Args:
            artist_id: The UUID of the artist to delete.
        """

        client = await SupabaseClient.get_client()
        client.table(self.TABLE).delete().eq("id", str(artist_id)).execute()


    async def find_by_user_id(self, user_id: UUID) -> Artist | None:
        """Find an artist associated with a given user account.

        Args:
            user_id: The UUID of the user account.

        Returns:
            The Artist entity if found, None otherwise.
        """

        client = await SupabaseClient.get_client()

        response = (
            client.table(self.TABLE)
            .select("*")
            .eq("user_id", str(user_id))
            .execute()
        )

        if not response.data:
            return None

        return map_to_artist(response.data[0])
```

```python
# infrastructure/persistence/supabase/mappers.py
from domain.entities.artist_entity import Artist


def map_to_artist(row: dict) -> Artist:
    """Convert a Supabase database row into a domain Artist entity.

    Args:
        row: Raw dictionary from Supabase query result.

    Returns:
        A fully hydrated Artist domain entity.
    """

    return Artist(
        id=row["id"],
        user_id=row["user_id"],
        bio=row["bio"],
        specialities=row["specialities"],
        instagram=row.get("instagram"),
        rating_avg=row.get("rating_avg", 0.0),
        is_active=row.get("is_active", True),
    )


def map_to_artist_dict(artist: Artist) -> dict:
    """Convert a domain Artist entity into a Supabase-compatible dictionary.

    Args:
        artist: The Artist domain entity to serialize.

    Returns:
        A dictionary ready for Supabase upsert operations.
    """

    return {
        "id": str(artist.id),
        "user_id": str(artist.user_id),
        "bio": artist.bio,
        "specialities": artist.specialities,
        "instagram": artist.instagram,
        "rating_avg": artist.rating_avg,
        "is_active": artist.is_active,
    }
```

### 5.4 Core Layer - Errors & Responses

```python
# core/errors/base_error.py


class BaseError(Exception):
    """Base error class for all application errors.

    All custom errors in the application inherit from this class
    to provide a consistent error interface with code and message.
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
```

```python
# core/errors/domain_errors.py
from core.errors.base_error import BaseError


class DomainError(BaseError):
    """Base error for domain layer violations.

    Raised when business rules are broken or entities are not found.
    """

    pass


class EntityNotFoundError(DomainError):
    """Raised when a requested entity does not exist in the system."""

    def __init__(self, message: str = "Entity not found") -> None:
        super().__init__(message, code="ENTITY_NOT_FOUND")


class BusinessRuleError(DomainError):
    """Raised when a business rule or invariant is violated."""

    def __init__(self, message: str = "Business rule violated") -> None:
        super().__init__(message, code="BUSINESS_RULE_ERROR")


class DuplicateEntityError(DomainError):
    """Raised when attempting to create an entity that already exists."""

    def __init__(self, message: str = "Entity already exists") -> None:
        super().__init__(message, code="DUPLICATE_ENTITY")
```

```python
# core/errors/application_errors.py
from core.errors.base_error import BaseError


class ApplicationError(BaseError):
    """Base error for application layer violations.

    Raised when application-level operations fail,
    such as validation errors or authorization issues.
    """

    pass


class ValidationError(ApplicationError):
    """Raised when input data fails validation rules."""

    def __init__(self, message: str = "Validation failed") -> None:
        super().__init__(message, code="VALIDATION_ERROR")


class UnauthorizedError(ApplicationError):
    """Raised when authentication is missing or invalid."""

    def __init__(self, message: str = "Unauthorized") -> None:
        super().__init__(message, code="UNAUTHORIZED")


class ForbiddenError(ApplicationError):
    """Raised when user lacks permission for the requested action."""

    def __init__(self, message: str = "Forbidden") -> None:
        super().__init__(message, code="FORBIDDEN")
```

```python
# core/errors/infrastructure_errors.py
from core.errors.base_error import BaseError


class InfrastructureError(BaseError):
    """Base error for infrastructure layer failures.

    Raised when external services or persistence operations fail.
    """

    pass


class DatabaseError(InfrastructureError):
    """Raised when a database operation fails."""

    def __init__(self, message: str = "Database error occurred") -> None:
        super().__init__(message, code="DATABASE_ERROR")


class ExternalServiceError(InfrastructureError):
    """Raised when an external service call fails.

    Args:
        service: Name of the external service (e.g., 'Stripe', 'Email').
        message: Description of what went wrong.
    """

    def __init__(self, service: str, message: str = "External service error") -> None:
        super().__init__(f"{service}: {message}", code="EXTERNAL_SERVICE_ERROR")
```

```python
# core/responses/success_response.py
from pydantic import BaseModel
from typing import Generic, TypeVar


T = TypeVar("T")


class SuccessResponse(BaseModel, Generic[T]):
    """Standard success response wrapper for all API endpoints.

    Provides a consistent response format with success flag,
    generic data payload, and optional message.
    """

    success: bool = True
    data: T
    message: str | None = None


class PaginatedResponse(BaseModel, Generic[T]):
    """Paginated response wrapper for list endpoints.

    Extends SuccessResponse with pagination metadata
    to support client-side navigation.
    """

    success: bool = True
    data: list[T]
    total: int
    page: int
    per_page: int
    total_pages: int
```

```python
# core/responses/error_response.py
from pydantic import BaseModel
from typing import Any


class ErrorResponse(BaseModel):
    """Standard error response wrapper for all API endpoints.

    Provides a consistent error format with success flag
    and structured error details.
    """

    success: bool = False
    error: ErrorDetail


class ErrorDetail(BaseModel):
    """Structured error information.

    Contains the error code, human-readable message,
    and optional additional details for debugging.
    """

    code: str
    message: str
    details: list[dict[str, Any]] | None = None
```

### 5.5 API Layer - Handler (usa Use Cases)

```python
# api/v1/endpoints/artist_handler.py
from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from application.queries.get_artist_query import GetArtistQuery
from application.commands.create_artist_command import CreateArtistCommand
from application.dto.requests.create_artist_request import CreateArtistRequest
from application.dto.responses.artist_response import ArtistResponse
from core.responses.success_response import SuccessResponse
from core.errors.domain_errors import EntityNotFoundError
from api.deps import get_current_admin_user


router = APIRouter(prefix="/artists", tags=["artists"])


@router.get("/{artist_id}", response_model=SuccessResponse[ArtistResponse])
async def get_artist(
    artist_id: UUID,
    query: GetArtistQuery = Depends(),
) -> SuccessResponse[ArtistResponse]:
    """Retrieve an artist by their unique identifier.

    This endpoint is publicly accessible and returns the artist's
    profile information including specialities and rating.

    Args:
        artist_id: The UUID of the artist to retrieve.
        query: Injected query handler for artist retrieval.

    Returns:
        A success response containing the artist data.

    Raises:
        HTTPException: 404 if the artist is not found.
    """

    try:
        artist = await query.execute(artist_id)

        return SuccessResponse(data=artist)

    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message)

@router.post("/", response_model=SuccessResponse[ArtistResponse], status_code=status.HTTP_201_CREATED)
async def create_artist(
    request: CreateArtistRequest,
    command: CreateArtistCommand = Depends(),
    _admin=Depends(get_current_admin_user),
):
    """Create a new artist (admin only)"""
    try:
        artist = await command.execute(request)
        return SuccessResponse(data=artist, message="Artist created successfully")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
```

### 5.6 Arquitectura Frontend

#### Estructura de Directorios - Web (React)

```
apps/web/
├── src/
│   ├── app/                          # App shell y configuración
│   │   ├── App.tsx                   # Componente raíz
│   │   ├── providers.tsx             # Providers globales (QueryClient, Router)
│   │   └── routes.tsx                # Configuración de rutas
│   │
│   ├── features/                     # Features organizadas por dominio
│   │   ├── auth/
│   │   │   ├── components/
│   │   │   │   ├── LoginForm.tsx
│   │   │   │   ├── RegisterForm.tsx
│   │   │   │   └── ProtectedRoute.tsx
│   │   │   ├── hooks/
│   │   │   │   ├── useAuth.ts
│   │   │   │   └── useLogin.ts
│   │   │   ├── services/
│   │   │   │   └── auth.service.ts
│   │   │   ├── stores/
│   │   │   │   └── auth.store.ts
│   │   │   └── types/
│   │   │       └── auth.types.ts
│   │   │
│   │   ├── artists/
│   │   │   ├── components/
│   │   │   │   ├── ArtistCard.tsx
│   │   │   │   ├── ArtistList.tsx
│   │   │   │   ├── ArtistDetail.tsx
│   │   │   │   ├── ArtistPortfolio.tsx
│   │   │   │   └── ArtistAvailability.tsx
│   │   │   ├── hooks/
│   │   │   │   ├── useArtists.ts
│   │   │   │   ├── useArtist.ts
│   │   │   │   └── useArtistPortfolio.ts
│   │   │   ├── services/
│   │   │   │   └── artist.service.ts
│   │   │   └── types/
│   │   │       └── artist.types.ts
│   │   │
│   │   ├── appointments/
│   │   │   ├── components/
│   │   │   │   ├── AppointmentCalendar.tsx
│   │   │   │   ├── AppointmentForm.tsx
│   │   │   │   ├── AppointmentCard.tsx
│   │   │   │   └── AppointmentDetails.tsx
│   │   │   ├── hooks/
│   │   │   │   ├── useAppointments.ts
│   │   │   │   └── useCreateAppointment.ts
│   │   │   ├── services/
│   │   │   │   └── appointment.service.ts
│   │   │   └── types/
│   │   │       └── appointment.types.ts
│   │   │
│   │   ├── consents/
│   │   │   ├── components/
│   │   │   │   ├── ConsentForm.tsx
│   │   │   │   ├── ConsentQR.tsx
│   │   │   │   └── SignaturePad.tsx
│   │   │   ├── hooks/
│   │   │   │   └── useConsent.ts
│   │   │   └── services/
│   │   │       └── consent.service.ts
│   │   │
│   │   └── dashboard/
│   │       ├── components/
│   │       │   ├── StatsCard.tsx
│   │       │   ├── RevenueChart.tsx
│   │       │   └── UpcomingAppointments.tsx
│   │       └── hooks/
│   │           └── useDashboard.ts
│   │
│   ├── shared/                       # Componentes y utilidades compartidas
│   │   ├── components/
│   │   │   ├── ui/                   # Componentes base (shadcn/ui)
│   │   │   │   ├── Button.tsx
│   │   │   │   ├── Input.tsx
│   │   │   │   ├── Card.tsx
│   │   │   │   ├── Dialog.tsx
│   │   │   │   ├── Table.tsx
│   │   │   │   └── ...
│   │   │   ├── layout/
│   │   │   │   ├── MainLayout.tsx
│   │   │   │   ├── Sidebar.tsx
│   │   │   │   ├── Header.tsx
│   │   │   │   └── Footer.tsx
│   │   │   └── feedback/
│   │   │       ├── Loading.tsx
│   │   │       ├── ErrorBoundary.tsx
│   │   │       └── EmptyState.tsx
│   │   ├── hooks/
│   │   │   ├── useDebounce.ts
│   │   │   ├── useMediaQuery.ts
│   │   │   └── usePagination.ts
│   │   ├── utils/
│   │   │   ├── format.ts             # Formateo de fechas, moneda, etc.
│   │   │   ├── validators.ts         # Validaciones comunes
│   │   │   └── helpers.ts
│   │   └── types/
│   │       └── common.types.ts
│   │
│   ├── lib/                          # Configuración de librerías
│   │   ├── api.ts                    # Instancia de Axios configurada
│   │   ├── query-client.ts           # Configuración TanStack Query
│   │   └── supabase.ts               # Cliente Supabase (si se usa auth)
│   │
│   └── styles/
│       ├── globals.css               # Estilos globales
│       └── tailwind.css              # Configuración Tailwind
│
├── public/
├── index.html
├── package.json
├── tailwind.config.js
├── tsconfig.json
├── vite.config.ts
└── .env.example
```

#### Estructura de Directorios - Mobile (React Native + Expo)

```
apps/mobile/
├── app/                              # Expo Router (file-based routing)
│   ├── _layout.tsx                   # Layout raíz (providers)
│   ├── (auth)/
│   │   ├── login.tsx
│   │   ├── register.tsx
│   │   └── _layout.tsx
│   ├── (tabs)/
│   │   ├── _layout.tsx               # Tab navigator
│   │   ├── index.tsx                 # Home/Dashboard
│   │   ├── artists.tsx               # Lista artistas
│   │   ├── appointments.tsx          # Mis citas
│   │   └── profile.tsx               # Mi perfil
│   ├── artist/
│   │   └── [id]/
│   │       ├── index.tsx             # Detalle artista
│   │       ├── portfolio.tsx         # Portafolio
│   │       └── book.tsx              # Reservar cita
│   ├── appointment/
│   │   ├── [id].tsx                  # Detalle cita
│   │   └── create.tsx                # Crear cita
│   └── consent/
│       └── [id].tsx                  # Firmar consentimiento
│
├── components/
│   ├── ui/                           # Componentes base
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   ├── Card.tsx
│   │   └── ...
│   ├── artists/
│   │   ├── ArtistCard.tsx
│   │   └── ArtistList.tsx
│   ├── appointments/
│   │   ├── AppointmentCard.tsx
│   │   └── CalendarView.tsx
│   └── shared/
│       ├── Loading.tsx
│       └── ErrorView.tsx
│
├── hooks/                            # Hooks compartidos con web
│   ├── useAuth.ts
│   ├── useArtists.ts
│   └── useAppointments.ts
│
├── services/                         # Servicios API (compartidos con web)
│   ├── auth.service.ts
│   ├── artist.service.ts
│   └── appointment.service.ts
│
├── stores/                           # Stores Zustand (compartidos con web)
│   ├── auth.store.ts
│   └── appointment.store.ts
│
├── types/                            # Tipos TypeScript (compartidos con web)
│   ├── artist.types.ts
│   ├── appointment.types.ts
│   └── ...
│
├── assets/
│   ├── images/
│   └── fonts/
│
├── app.json                          # Config Expo
├── package.json
├── tsconfig.json
└── .env.example
```

#### Patrones de Diseño Frontend

**1. Feature-Based Structure**
Cada feature agrupa sus componentes, hooks, servicios y tipos:
```
features/artists/
├── components/    # Componentes específicos de artistas
├── hooks/         # Hooks de artistas
├── services/      # Llamadas a API de artistas
└── types/         # Tipos de artistas
```

**2. Custom Hooks (Data Fetching)**
```typescript
// features/artists/hooks/useArtists.ts
import { useQuery } from '@tanstack/react-query';
import { artistService } from '../services/artist.service';
import type { ArtistFilters } from '../types/artist.types';

export function useArtists(filters?: ArtistFilters) {
  return useQuery({
    queryKey: ['artists', filters],
    queryFn: () => artistService.list(filters),
  });
}

export function useArtist(id: string) {
  return useQuery({
    queryKey: ['artists', id],
    queryFn: () => artistService.getById(id),
    enabled: !!id,
  });
}
```

**3. Services (API Layer)**
```typescript
// features/artists/services/artist.service.ts
import { api } from '@/lib/api';
import type { Artist, ArtistFilters } from '../types/artist.types';

export const artistService = {
  list: (filters?: ArtistFilters) =>
    api.get<Artist[]>('/artists', { params: filters }),

  getById: (id: string) =>
    api.get<Artist>(`/artists/${id}`),

  getPortfolio: (id: string) =>
    api.get(`/artists/${id}/portfolio`),

  getAvailability: (id: string, date: string) =>
    api.get(`/artists/${id}/availability`, { params: { date } }),
};
```

**4. Zustand Store (Estado Global)**
```typescript
// features/auth/stores/auth.store.ts
import { create } from 'zustand';
import { persist } from 'zustand/middleware';
import type { User } from '../types/auth.types';

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  login: (user: User, token: string) => void;
  logout: () => void;
  updateUser: (user: Partial<User>) => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      login: (user, token) => set({ user, token, isAuthenticated: true }),
      logout: () => set({ user: null, token: null, isAuthenticated: false }),
      updateUser: (data) =>
        set((state) => ({
          user: state.user ? { ...state.user, ...data } : null,
        })),
    }),
    { name: 'auth-storage' }
  )
);
```

**5. API Client Configuration**
```typescript
// lib/api.ts
import axios from 'axios';
import { useAuthStore } from '@/features/auth/stores/auth.store';

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1',
  headers: { 'Content-Type': 'application/json' },
});

// Interceptor para añadir token
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para manejar errores 401
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

**6. Component Pattern (Presentational + Container)**
```tsx
// features/artists/components/ArtistCard.tsx (Presentacional)
interface ArtistCardProps {
  artist: Artist;
  onSelect: (id: string) => void;
}

export function ArtistCard({ artist, onSelect }: ArtistCardProps) {
  return (
    <Card onClick={() => onSelect(artist.id)}>
      <img src={artist.avatarUrl} alt={artist.name} />
      <h3>{artist.name}</h3>
      <p>{artist.specialities.join(', ')}</p>
      <span>⭐ {artist.ratingAvg.toFixed(1)}</span>
    </Card>
  );
}

// features/artists/components/ArtistList.tsx (Container)
export function ArtistList() {
  const { data: artists, isLoading, error } = useArtists();
  const navigate = useNavigate();

  if (isLoading) return <Loading />;
  if (error) return <ErrorBoundary error={error} />;

  return (
    <div className="grid grid-cols-3 gap-4">
      {artists?.map((artist) => (
        <ArtistCard
          key={artist.id}
          artist={artist}
          onSelect={(id) => navigate(`/artists/${id}`)}
        />
      ))}
    </div>
  );
}
```

#### Testing Frontend

```bash
# Web
cd apps/web
npm run test                    # Vitest
npm run test:e2e               # Playwright

# Mobile
cd apps/mobile
npm run test                    # Jest
npm run test:e2e               # Detox
```

**Estructura de tests:**
```
features/artists/
├── components/
│   └── ArtistCard.test.tsx
├── hooks/
│   └── useArtists.test.ts
└── services/
    └── artist.service.test.ts
```

### 5.7 Control de Errores y Logging

#### Arquitectura del Control de Errores

```
┌─────────────────────────────────────────────────────────────────┐
│                        API Layer (FastAPI)                       │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              Global Exception Handler                      │  │
│  │  Captura TODAS las excepciones y las convierte en         │  │
│  │  respuestas HTTP consistentes con ErrorResponse           │  │
│  └───────────────────────────────────────────────────────────┘  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
        ▼                   ▼                   ▼
┌───────────────┐  ┌────────────────┐  ┌────────────────┐
│ Domain Errors │  │Application Err│  │Infrastructure  │
│ (404, 409,   │  │ (400, 401,    │  │   Errors       │
│  422)        │  │  403)         │  │ (500, 502,     │
│              │  │               │  │  503)          │
└───────────────┘  └────────────────┘  └────────────────┘
```

#### Global Exception Handler (FastAPI)

```python
# api/middleware/error_handler.py
import logging
import traceback
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from core.errors.base_error import BaseError
from core.errors.domain_errors import DomainError
from core.errors.application_errors import ApplicationError
from core.errors.infrastructure_errors import InfrastructureError
from core.responses.error_response import ErrorResponse, ErrorDetail


logger = logging.getLogger(__name__)


def register_error_handlers(app: FastAPI) -> None:
    """Register global exception handlers for the FastAPI application.

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
        """

        # Determine HTTP status code based on error type
        status_code = _get_status_code(exc)

        # Log the error with context
        _log_error(request, exc, status_code)

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
    async def handle_unhandled_exception(request: Request, exc: Exception) -> JSONResponse:
        """Handle any unhandled exceptions.

        Catches unexpected errors, logs them with full traceback,
        and returns a generic 500 error to the client.
        """

        # Log the full traceback for debugging
        logger.error(
            "Unhandled exception",
            extra={
                "path": request.url.path,
                "method": request.method,
                "error_type": type(exc).__name__,
                "error_message": str(exc),
                "traceback": traceback.format_exc(),
            },
        )

        # Return generic error to client (never expose internals)
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


def _get_status_code(exc: BaseError) -> int:
    """Map error types to HTTP status codes.

    Args:
        exc: The exception to map.

    Returns:
        The appropriate HTTP status code.
    """

    if isinstance(exc, DomainError):
        return _get_domain_status_code(exc)

    if isinstance(exc, ApplicationError):
        return _get_application_status_code(exc)

    if isinstance(exc, InfrastructureError):
        return _get_infrastructure_status_code(exc)

    return 500


def _get_domain_status_code(exc: DomainError) -> int:
    """Map domain errors to HTTP status codes."""

    from core.errors.domain_errors import (
        EntityNotFoundError,
        BusinessRuleError,
        DuplicateEntityError,
    )

    if isinstance(exc, EntityNotFoundError):
        return 404

    if isinstance(exc, DuplicateEntityError):
        return 409

    if isinstance(exc, BusinessRuleError):
        return 422

    return 400


def _get_application_status_code(exc: ApplicationError) -> int:
    """Map application errors to HTTP status codes."""

    from core.errors.application_errors import (
        ValidationError,
        UnauthorizedError,
        ForbiddenError,
    )

    if isinstance(exc, UnauthorizedError):
        return 401

    if isinstance(exc, ForbiddenError):
        return 403

    if isinstance(exc, ValidationError):
        return 422

    return 400


def _get_infrastructure_status_code(exc: InfrastructureError) -> int:
    """Map infrastructure errors to HTTP status codes."""

    from core.errors.infrastructure_errors import (
        DatabaseError,
        ExternalServiceError,
    )

    if isinstance(exc, ExternalServiceError):
        return 502

    if isinstance(exc, DatabaseError):
        return 500

    return 503


def _log_error(request: Request, exc: BaseError, status_code: int) -> None:
    """Log an error with request context.

    Args:
        request: The HTTP request that caused the error.
        exc: The exception that was raised.
        status_code: The HTTP status code being returned.
    """

    log_data = {
        "path": request.url.path,
        "method": request.method,
        "status_code": status_code,
        "error_code": exc.code,
        "error_message": exc.message,
        "error_type": type(exc).__name__,
    }

    if status_code >= 500:
        logger.error("Server error", extra=log_data)
    elif status_code >= 400:
        logger.warning("Client error", extra=log_data)
```

#### Logging Estructurado

```python
# core/logging.py
import logging
import sys
import json
from datetime import datetime
from typing import Any


class StructuredFormatter(logging.Formatter):
    """Custom formatter that outputs structured JSON logs.

    Produces machine-readable logs with consistent fields
    for easy parsing by log aggregation tools (ELK, Datadog, etc.)
    """

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record as a JSON string.

        Args:
            record: The log record to format.

        Returns:
            A JSON string with structured log data.
        """

        log_data: dict[str, Any] = {
            "timestamp": datetime.utcnow().isoformat(),
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
        log_level: The minimum log level to output.
    """

    # Create structured formatter
    formatter = StructuredFormatter()

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level.upper()))

    # Console handler with structured output
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Suppress noisy library loggers
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("supabase").setLevel(logging.WARNING)
```

#### Ejemplo de Log Estructurado

```json
{
  "timestamp": "2026-05-08T14:30:00.000Z",
  "level": "ERROR",
  "logger": "api.middleware.error_handler",
  "message": "Server error",
  "data": {
    "path": "/api/v1/appointments",
    "method": "POST",
    "status_code": 500,
    "error_code": "DATABASE_ERROR",
    "error_message": "Failed to insert appointment: connection timeout",
    "error_type": "DatabaseError"
  }
}
```

#### Error Handling en Frontend

```typescript
// lib/error-handler.ts
import { AxiosError } from 'axios';
import { toast } from '@/components/ui/Toast';

/** Structured error from the API */
interface ApiError {
  success: false;
  error: {
    code: string;
    message: string;
    details?: Record<string, unknown>[];
  };
}

/** Map of error codes to user-friendly messages */
const ERROR_MESSAGES: Record<string, string> = {
  ENTITY_NOT_FOUND: 'The requested resource was not found.',
  BUSINESS_RULE_ERROR: 'This operation violates a business rule.',
  VALIDATION_ERROR: 'Please check your input and try again.',
  UNAUTHORIZED: 'Please log in to continue.',
  FORBIDDEN: 'You do not have permission to perform this action.',
  INTERNAL_SERVER_ERROR: 'Something went wrong. Please try again later.',
};


export function handleApiError(error: unknown): never {
  """Handle API errors and show appropriate user notifications.

  Args:
    error: The error from an API call (AxiosError or unknown).

  Raises:
    The original error after handling.
  """

  if (error instanceof AxiosError && error.response?.data) {
    const apiError = error.response.data as ApiError;
    const errorCode = apiError.error?.code;
    const errorMessage = ERROR_MESSAGES[errorCode] || apiError.error?.message;

    // Show user-friendly toast notification
    toast.error(errorMessage);

    // Log to console for debugging
    console.error('[API Error]', {
      code: errorCode,
      message: apiError.error?.message,
      path: error.config?.url,
      status: error.response?.status,
    });

    // Throw specific error for callers to handle
    throw new ApiErrorException(errorCode, errorMessage);
  }

  // Network or unknown errors
  toast.error('Network error. Please check your connection.');
  console.error('[Network Error]', error);

  throw error;
}


export class ApiErrorException extends Error {
  """Custom error class for API errors in the frontend."""

  code: string;

  constructor(code: string, message: string) {
    super(message);
    this.code = code;
    this.name = 'ApiErrorException';
  }
}
```

```typescript
// lib/api.ts - Axios instance with error interceptor
import axios from 'axios';
import { handleApiError } from './error-handler';
import { useAuthStore } from '@/features/auth/stores/auth.store';


export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  timeout: 10000,
});


// Request interceptor: attach auth token
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});


// Response interceptor: handle errors globally
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Handle 401: redirect to login
    if (error.response?.status === 401) {
      useAuthStore.getState().logout();
      window.location.href = '/login';
      return Promise.reject(error);
    }

    // Handle all other errors
    return handleApiError(error);
  }
);
```

```tsx
// components/ui/ErrorBoundary.tsx
import { Component, ErrorInfo, ReactNode } from 'react';


interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}


interface State {
  hasError: boolean;
  error: Error | null;
}


export class ErrorBoundary extends Component<Props, State> {
  """Catches React rendering errors and displays a fallback UI.

  Prevents the entire app from crashing when a component fails.
  Logs the error for debugging with component stack trace.
  """

  state: State = { hasError: false, error: null };


  static getDerivedStateFromError(error: Error): State {
    """Update state when an error is caught."""

    return { hasError: true, error };
  }


  componentDidCatch(error: Error, errorInfo: ErrorInfo): void {
    """Log the error with component stack trace."""

    console.error('[ErrorBoundary]', {
      error: error.message,
      stack: error.stack,
      componentStack: errorInfo.componentStack,
    });
  }


  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="error-fallback">
          <h2>Something went wrong</h2>
          <p>{this.state.error?.message}</p>
          <button onClick={() => this.setState({ hasError: false, error: null })}>
            Try again
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
```

## 6. Modelo de Base de Datos (Supabase)

### Diagrama Entidad-Relación

```
┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│    users     │     │   artists    │  1  │  portfolios  │
├──────────────┤     ├──────────────┤────>├──────────────┤
│ id (PK)      │<─── │ id (PK)      │     │ id (PK)      │
│ email        │     │ user_id (FK) │     │ artist_id FK │
│ password_hash│     │ bio          │     │ image_url    │
│ full_name    │     │ specialities │     │ style        │
│ phone        │     │ instagram    │     │ description  │
│ role         │     │ rating_avg   │     │ created_at   │
│ avatar_url   │     │ is_active    │     └──────────────┘
│ created_at   │     │ created_at   │
│ updated_at   │     └──────────────┘
└──────┬───────┘            │
       │              ┌─────┴─────────┐
       │              │ availability  │
       │              ├───────────────┤
       │              │ id (PK)       │
       │              │ artist_id (FK)│
       │              │ day_of_week   │
       │              │ start_time    │
       │              │ end_time      │
       │              │ is_active     │
       │              └───────────────┘
       │
       │         ┌──────────────────┐     ┌──────────────┐
       └────────>│  appointments    │     │   payments   │
                 ├──────────────────┤     ├──────────────┤
                 │ id (PK)          │────>│ id (PK)      │
                 │ client_id (FK)   │     │ appointment_id│
                 │ artist_id (FK)   │     │ amount       │
                 │ date             │     │ type         │
                 │ start_time       │     │ status       │
                 │ end_time         │     │ stripe_id    │
                 │ service_type     │     │ created_at   │
                 │ status           │     └──────────────┘
                 │ notes            │
                 │ deposit_amount   │     ┌──────────────┐
                 │ total_price      │     │notifications │
                 │ created_at       │     ├──────────────┤
                 │ updated_at       │     │ id (PK)      │
                 └──────────────────┘     │ user_id (FK) │
                                          │ type         │
                                          │ title        │
                 ┌──────────────────┐     │ message      │
                 │   reviews        │     │ is_read      │
                 ├──────────────────┤     │ created_at   │
                 │ id (PK)          │     └──────────────┘
                 │ appointment_id FK│
                 │ client_id (FK)   │
                 │ artist_id (FK)   │
                 │ rating (1-5)     │
                 │ comment          │
                 │ created_at       │
                 └──────────────────┘
```

### Enums

```python
class UserRole(str, Enum):
    CLIENT = "client"
    ARTIST = "artist"
    ADMIN = "admin"

class AppointmentStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"

class PaymentType(str, Enum):
    DEPOSIT = "deposit"
    FULL = "full"
    REMAINING = "remaining"

class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class TattooStyle(str, Enum):
    REALISTIC = "realistic"
    TRADITIONAL = "traditional"
    JAPANESE = "japanese"
    MINIMALIST = "minimalist"
    GEOMETRIC = "geometric"
    WATERCOLOR = "watercolor"
    TRIBAL = "tribal"
    BLACKWORK = "blackwork"
    DOTWORK = "dotwork"
    NEO_TRADITIONAL = "neo_traditional"
```

## 7. Diseño de la API REST

### Endpoints Principales (v1)

```
# Autenticación
POST   /api/v1/auth/register          # Registro de usuario
POST   /api/v1/auth/login             # Login
POST   /api/v1/auth/refresh           # Refrescar token
POST   /api/v1/auth/forgot-password   # Recuperar contraseña
POST   /api/v1/auth/reset-password    # Resetear contraseña

# Usuarios
GET    /api/v1/users/me               # Perfil propio
PUT    /api/v1/users/me               # Actualizar perfil
PUT    /api/v1/users/me/avatar        # Subir avatar

# Artistas
GET    /api/v1/artists                # Listar artistas (público)
GET    /api/v1/artists/{id}           # Detalle de artista
GET    /api/v1/artists/{id}/portfolio # Portafolio del artista
GET    /api/v1/artists/{id}/reviews   # Reseñas del artista
GET    /api/v1/artists/{id}/availability # Disponibilidad

# Citas
POST   /api/v1/appointments           # Crear cita
GET    /api/v1/appointments           # Listar citas (propias)
GET    /api/v1/appointments/{id}      # Detalle de cita
PUT    /api/v1/appointments/{id}/accept   # Aceptar cita (artista)
PUT    /api/v1/appointments/{id}/reject   # Rechazar cita (artista)
PUT    /api/v1/appointments/{id}/cancel   # Cancelar cita
PUT    /api/v1/appointments/{id}/complete # Completar cita

# Pagos
POST   /api/v1/payments               # Crear pago
GET    /api/v1/payments               # Listar pagos (propios)
GET    /api/v1/payments/{id}          # Detalle de pago
POST   /api/v1/payments/{id}/refund   # Solicitar reembolso

# Consentimientos
POST   /api/v1/consents               # Crear consentimiento
GET    /api/v1/consents/{id}          # Detalle de consentimiento
POST   /api/v1/consents/{id}/sign     # Firmar consentimiento (QR/remote)

# Notificaciones
GET    /api/v1/notifications          # Listar notificaciones
PUT    /api/v1/notifications/{id}/read # Marcar como leída
PUT    /api/v1/notifications/read-all  # Marcar todas como leídas

# Admin
GET    /api/v1/admin/dashboard        # Dashboard (stats)
GET    /api/v1/admin/appointments     # Todas las citas
GET    /api/v1/admin/payments         # Todos los pagos
GET    /api/v1/admin/reports/financial # Reporte financiero
POST   /api/v1/admin/artists          # Crear artista
PUT    /api/v1/admin/artists/{id}     # Editar artista
DELETE /api/v1/admin/artists/{id}     # Desactivar artista
PUT    /api/v1/admin/settings         # Configuración del estudio
```

## 8. Autenticación y Autorización

### Flujo JWT

```
1. Login → POST /auth/login {email, password}
2. Backend valida credenciales → retorna {access_token, refresh_token}
3. Frontend almacena tokens (httpOnly cookie o secure storage)
4. Requests incluyen Authorization: Bearer <access_token>
5. Si access_token expira → POST /auth/refresh con refresh_token
6. Si refresh_token expira → re-login requerido
```

### Matriz de Permisos

| Recurso | Cliente | Artista | Admin |
|---------|---------|---------|-------|
| Ver artistas | ✅ | ✅ | ✅ |
| Crear cita | ✅ | ❌ | ✅ |
| Ver citas propias | ✅ | ✅ | ✅ |
| Ver todas citas | ❌ | ❌ | ✅ |
| Aceptar/rechazar cita | ❌ | ✅ | ✅ |
| Subir portafolio | ❌ | ✅ | ✅ |
| Ver pagos propios | ✅ | ✅ | ✅ |
| Ver todos pagos | ❌ | ❌ | ✅ |
| Gestionar artistas | ❌ | ❌ | ✅ |
| Configurar estudio | ❌ | ❌ | ✅ |

## 9. Estrategia de Notificaciones

### Canales
- **Email**: SendGrid / Resend (transactional emails)
- **Push**: Expo Notifications (móvil) + Web Push API (web)
- **In-App**: Supabase Realtime

### Cola de Tareas
- Celery + Redis para envío asíncrono de notificaciones
- Tareas programadas para recordatorios (48h, 24h, 2h antes)
- Retry automático en caso de fallo

## 10. Variables de Entorno

```env
# Supabase
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJxxxxxx
SUPABASE_SERVICE_KEY=eyJxxxxxx

# Backend
SECRET_KEY=<random-secret>
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Redis
REDIS_URL=redis://localhost:6379/0

# Pagos
STRIPE_SECRET_KEY=sk_test_xxx
STRIPE_WEBHOOK_SECRET=whsec_xxx

# Email
SENDGRID_API_KEY=SG.xxx
EMAIL_FROM=noreply@tattostudio.com

# Google Calendar
GOOGLE_CALENDAR_CREDENTIALS_JSON=path/to/credentials.json

# Frontend
VITE_API_URL=http://localhost:8000/api/v1
EXPO_PUBLIC_API_URL=http://localhost:8000/api/v1
```

## 11. Desarrollo Local

### Prerrequisitos
- Python 3.11+
- Node.js 20+
- Docker Desktop
- Expo CLI
- Cuenta en Supabase

### Inicio rápido
```bash
# Backend
cd backend
python -m venv venv
pip install -r requirements.txt
uvicorn src.api.main:app --reload

# Web
cd apps/web
npm install
npm run dev

# Mobile
cd apps/mobile
npm install
npx expo start

# Docker (Redis)
docker-compose up -d
```

## 12. Decisiones Técnicas Clave

| Decisión | Alternativas | Elección | Razón |
|----------|-------------|----------|-------|
| Arquitectura | MVC, Hexagonal | Clean Architecture + CQRS | Separación clara, testeable, escalable |
| Interfaces | ABC, Protocol | Protocol (typing) | Nativo de Python, duck typing, sin herencia |
| Base de datos | PostgreSQL directo, SQLAlchemy | Supabase | Managed, Auth integrado, Storage, Realtime |
| Monorepo | Multi-repo | Monorepo (Turborepo/Nx) | Compartir código entre apps |
| Estado global | Redux, Context | Zustand | Simplicidad, TS nativo, pequeño bundle |
| UI Web | MUI, Chakra | Tailwind + shadcn/ui | Personalización, consistencia, rendimiento |
| Auth | OAuth, Session | JWT stateless | Escalabilidad, multi-plataforma |
| Pagos | PayPal, manual | Stripe | API robusta, soporte global, webhooks |
| Email | Manual, third-party | SendGrid / SMTP | Sencillo, fiable, escalable |
