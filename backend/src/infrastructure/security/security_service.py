"""Security service for password hashing and JWT token management.

This module provides cryptographic operations for the TattoStudioApp,
including password hashing with PBKDF2-SHA256 and JWT token creation/verification.

Uses python-jose for JWT operations and passlib for password hashing.
"""

import logging
from datetime import UTC, datetime, timedelta
from uuid import UUID

from jose import JWTError, jwt
from passlib.context import CryptContext

from core.config import settings
from core.errors import UnauthorizedError

logger = logging.getLogger(__name__)

# Password hashing context using PBKDF2-SHA256
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


class SecurityService:
    """Service for password hashing and JWT token operations.

    Provides methods for hashing/verifying passwords and creating/decoding
    JWT tokens for authentication and authorization.

    Attributes:
        _secret_key: Secret key for JWT signing.
        _algorithm: JWT algorithm (HS256).
        _access_token_expire_minutes: Access token validity in minutes.
        _refresh_token_expire_days: Refresh token validity in days.
    """

    def __init__(self) -> None:
        """Initialize the security service with configuration values."""

        self._secret_key = settings.SECRET_KEY
        self._algorithm = settings.JWT_ALGORITHM
        self._access_token_expire_minutes = settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        self._refresh_token_expire_days = settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS

    def hash_password(self, password: str) -> str:
        """Hash a plain text password using PBKDF2-SHA256.

        Args:
            password: The plain text password to hash.

        Returns:
            The PBKDF2-SHA256 hashed password string.
        """

        return pwd_context.hash(password)


    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a plain text password against a PBKDF2-SHA256 hash.

        Args:
            plain_password: The plain text password to verify.
            hashed_password: The PBKDF2-SHA256 hash to compare against.

        Returns:
            True if the password matches, False otherwise.
        """

        return pwd_context.verify(plain_password, hashed_password)


    def create_access_token(self, user_id: UUID, role: str) -> str:
        """Create a short-lived JWT access token.

        Args:
            user_id: The UUID of the authenticated user.
            role: The user's role string (e.g., "client", "artist", "admin").

        Returns:
            The encoded JWT access token string.
        """

        expire = datetime.now(UTC) + timedelta(
            minutes=self._access_token_expire_minutes
        )

        payload = {
            "sub": str(user_id),
            "role": role,
            "type": "access",
            "exp": expire,
            "iat": datetime.now(UTC),
        }

        token = jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

        logger.debug(
            "Access token created",
            extra={"extra_data": {"user_id": str(user_id), "role": role}},
        )

        return token


    def create_refresh_token(self, user_id: UUID) -> str:
        """Create a long-lived JWT refresh token.

        Args:
            user_id: The UUID of the authenticated user.

        Returns:
            The encoded JWT refresh token string.
        """

        expire = datetime.now(UTC) + timedelta(
            days=self._refresh_token_expire_days
        )

        payload = {
            "sub": str(user_id),
            "type": "refresh",
            "exp": expire,
            "iat": datetime.now(UTC),
        }

        token = jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

        logger.debug(
            "Refresh token created",
            extra={"extra_data": {"user_id": str(user_id)}},
        )

        return token


    def decode_token(self, token: str) -> dict:
        """Decode and validate a JWT token.

        Args:
            token: The JWT token string to decode.

        Returns:
            The decoded token payload dictionary.

        Raises:
            UnauthorizedError: If the token is invalid or expired.
        """

        try:
            payload = jwt.decode(
                token, self._secret_key, algorithms=[self._algorithm]
            )

            return payload

        except JWTError as e:
            logger.warning(
                "Invalid token",
                extra={"extra_data": {"error": str(e)}},
            )
            raise UnauthorizedError("Invalid or expired token") from e


# Singleton instance for convenience
security_service = SecurityService()
