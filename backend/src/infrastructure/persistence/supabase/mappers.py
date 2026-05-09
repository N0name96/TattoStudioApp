"""Mappers for converting between Supabase rows and domain entities.

This module provides bidirectional mapping functions between
the database representation (dict from Supabase) and the
domain entities used by the application.
"""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from domain.entities.appointment_entity import Appointment
from domain.entities.artist_entity import Artist
from domain.entities.cash_transaction_entity import CashTransaction
from domain.entities.client_entity import Client
from domain.entities.consent_entity import Consent
from domain.entities.payment_entity import Payment
from domain.entities.product_entity import Product
from domain.entities.user_entity import User
from domain.enums.appointment_status import AppointmentStatus
from domain.enums.cash_transaction_type import CashTransactionType
from domain.enums.client_source import ClientSource
from domain.enums.consent_status import ConsentStatus
from domain.enums.consent_type import ConsentType
from domain.enums.image_rights import ImageRights
from domain.enums.payment_status import PaymentStatus
from domain.enums.payment_type import PaymentType
from domain.enums.product_category import ProductCategory
from domain.enums.service_type import ServiceType
from domain.enums.user_role import UserRole
from domain.value_objects.money_vo import Money


def _parse_optional_datetime(value: str | None) -> datetime | None:
    if value is None:
        return None
    return datetime.fromisoformat(value)


# =============================================================================
# Appointment
# =============================================================================

def map_to_appointment(row: dict) -> Appointment:
    return Appointment(
        id=UUID(row["id"]),
        client_id=UUID(row["client_id"]),
        artist_id=UUID(row["artist_id"]),
        service_type=ServiceType(row["service_type"]),
        date=datetime.fromisoformat(row["date"]).date(),
        start_time=datetime.fromisoformat(row["start_time"]).time(),
        end_time=datetime.fromisoformat(row["end_time"]).time(),
        status=AppointmentStatus(row["status"]),
        notes=row.get("notes"),
        total_price=float(row.get("total_price", 0.0)),
        created_at=datetime.fromisoformat(row["created_at"]),
        updated_at=datetime.fromisoformat(row["updated_at"]),
    )


def map_to_appointment_dict(appointment: Appointment) -> dict:
    return {
        "id": str(appointment.id),
        "client_id": str(appointment.client_id),
        "artist_id": str(appointment.artist_id),
        "service_type": appointment.service_type.value,
        "date": appointment.date.isoformat(),
        "start_time": appointment.start_time.isoformat(),
        "end_time": appointment.end_time.isoformat(),
        "status": appointment.status.value,
        "notes": appointment.notes,
        "total_price": appointment.total_price,
        "created_at": appointment.created_at.isoformat(),
        "updated_at": appointment.updated_at.isoformat(),
    }


# =============================================================================
# User
# =============================================================================

def map_to_user(row: dict) -> User:
    return User(
        id=UUID(row["id"]),
        email=row["email"],
        hashed_password=row["hashed_password"],
        full_name=row["full_name"],
        role=UserRole(row["role"]),
        phone=row.get("phone"),
        is_active=row["is_active"],
        created_at=datetime.fromisoformat(row["created_at"]),
        updated_at=datetime.fromisoformat(row["updated_at"]),
    )


def map_to_user_dict(user: User) -> dict:
    return {
        "id": str(user.id),
        "email": user.email,
        "hashed_password": user.hashed_password,
        "full_name": user.full_name,
        "role": user.role.value,
        "phone": user.phone,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat(),
        "updated_at": user.updated_at.isoformat(),
    }


# =============================================================================
# Artist
# =============================================================================

def map_to_artist(row: dict) -> Artist:
    return Artist(
        id=UUID(row["id"]),
        name=row["name"],
        specialty=row["specialty"],
        email=row["email"],
        phone=row.get("phone"),
        bio=row.get("bio"),
        is_active=row["is_active"],
        created_at=datetime.fromisoformat(row["created_at"]),
        updated_at=datetime.fromisoformat(row["updated_at"]),
    )


def map_to_artist_dict(artist: Artist) -> dict:
    return {
        "id": str(artist.id),
        "name": artist.name,
        "specialty": artist.specialty,
        "email": artist.email,
        "phone": artist.phone,
        "bio": artist.bio,
        "is_active": artist.is_active,
        "created_at": artist.created_at.isoformat(),
        "updated_at": artist.updated_at.isoformat(),
    }


# =============================================================================
# Cash Transaction
# =============================================================================

def map_to_cash_transaction(row: dict) -> CashTransaction:
    return CashTransaction(
        id=UUID(row["id"]),
        amount=Decimal(str(row["amount"])),
        transaction_type=CashTransactionType(row["transaction_type"]),
        description=row.get("description"),
        appointment_id=UUID(row["appointment_id"]) if row.get("appointment_id") else None,
        created_at=datetime.fromisoformat(row["created_at"]),
        updated_at=datetime.fromisoformat(row["updated_at"]),
    )


def map_to_cash_transaction_dict(ct: CashTransaction) -> dict:
    return {
        "id": str(ct.id),
        "amount": str(ct.amount),
        "transaction_type": ct.transaction_type.value,
        "description": ct.description,
        "appointment_id": str(ct.appointment_id) if ct.appointment_id else None,
        "created_at": ct.created_at.isoformat(),
        "updated_at": ct.updated_at.isoformat(),
    }


# =============================================================================
# Client
# =============================================================================

def map_to_client(row: dict) -> Client:
    return Client(
        id=UUID(row["id"]),
        full_name=row["full_name"],
        email=row["email"],
        phone=row.get("phone"),
        birth_date=datetime.fromisoformat(row["birth_date"]).date() if row.get("birth_date") else None,
        source=ClientSource(row["source"]) if row.get("source") else None,
        image_rights=ImageRights(row["image_rights"]) if row.get("image_rights") else None,
        notes=row.get("notes"),
        is_active=row["is_active"],
        created_at=datetime.fromisoformat(row["created_at"]),
        updated_at=datetime.fromisoformat(row["updated_at"]),
    )


def map_to_client_dict(client: Client) -> dict:
    return {
        "id": str(client.id),
        "full_name": client.full_name,
        "email": client.email,
        "phone": client.phone,
        "birth_date": client.birth_date.isoformat() if client.birth_date else None,
        "source": client.source.value if client.source else None,
        "image_rights": client.image_rights.value if client.image_rights else None,
        "notes": client.notes,
        "is_active": client.is_active,
        "created_at": client.created_at.isoformat(),
        "updated_at": client.updated_at.isoformat(),
    }


# =============================================================================
# Consent
# =============================================================================

def map_to_consent(row: dict) -> Consent:
    return Consent(
        id=UUID(row["id"]),
        client_id=UUID(row["client_id"]),
        appointment_id=UUID(row["appointment_id"]) if row.get("appointment_id") else None,
        consent_type=ConsentType(row["consent_type"]),
        status=ConsentStatus(row["status"]),
        token=row["token"],
        signature_data=row.get("signature_data"),
        signed_at=_parse_optional_datetime(row.get("signed_at")),
        expires_at=datetime.fromisoformat(row["expires_at"]),
        created_at=datetime.fromisoformat(row["created_at"]),
        updated_at=datetime.fromisoformat(row["updated_at"]),
    )


def map_to_consent_dict(consent: Consent) -> dict:
    return {
        "id": str(consent.id),
        "client_id": str(consent.client_id),
        "appointment_id": str(consent.appointment_id) if consent.appointment_id else None,
        "consent_type": consent.consent_type.value,
        "status": consent.status.value,
        "token": consent.token,
        "signature_data": consent.signature_data,
        "signed_at": consent.signed_at.isoformat() if consent.signed_at else None,
        "expires_at": consent.expires_at.isoformat(),
        "created_at": consent.created_at.isoformat(),
        "updated_at": consent.updated_at.isoformat(),
    }


# =============================================================================
# Payment
# =============================================================================

def map_to_payment(row: dict) -> Payment:
    return Payment(
        id=UUID(row["id"]),
        appointment_id=UUID(row["appointment_id"]),
        amount=Decimal(str(row["amount"])),
        payment_type=PaymentType(row["payment_type"]),
        status=PaymentStatus(row["status"]),
        stripe_payment_id=row.get("stripe_payment_id"),
        created_at=datetime.fromisoformat(row["created_at"]),
        updated_at=datetime.fromisoformat(row["updated_at"]),
    )


def map_to_payment_dict(payment: Payment) -> dict:
    return {
        "id": str(payment.id),
        "appointment_id": str(payment.appointment_id),
        "amount": str(payment.amount),
        "payment_type": payment.payment_type.value,
        "status": payment.status.value,
        "stripe_payment_id": payment.stripe_payment_id,
        "created_at": payment.created_at.isoformat(),
        "updated_at": payment.updated_at.isoformat(),
    }


# =============================================================================
# Product
# =============================================================================

def map_to_product(row: dict) -> Product:
    return Product(
        id=UUID(row["id"]),
        name=row["name"],
        description=row.get("description"),
        category=ProductCategory(row["category"]),
        price=Money(amount=Decimal(str(row["price"]))),
        cost_price=Money(amount=Decimal(str(row["cost_price"]))),
        stock=int(row["stock"]),
        min_stock=int(row["min_stock"]),
        barcode=row.get("barcode"),
        is_active=row["is_active"],
        created_at=datetime.fromisoformat(row["created_at"]),
        updated_at=datetime.fromisoformat(row["updated_at"]),
    )


def map_to_product_dict(product: Product) -> dict:
    return {
        "id": str(product.id),
        "name": product.name,
        "description": product.description,
        "category": product.category.value,
        "price": str(product.price.amount),
        "cost_price": str(product.cost_price.amount),
        "stock": product.stock,
        "min_stock": product.min_stock,
        "barcode": product.barcode,
        "is_active": product.is_active,
        "created_at": product.created_at.isoformat(),
        "updated_at": product.updated_at.isoformat(),
    }
