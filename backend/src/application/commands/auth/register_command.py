"""Command to register a new user in the TattoStudioApp.

This command handles the user registration flow:
1. Check email uniqueness
2. Hash the password
3. Create the domain entity
4. Persist to repository
5. Return response DTO
"""

import logging

from application.dto.requests.auth.register_request import RegisterRequest
from application.dto.responses.auth.user_response import UserResponse
from core.errors import DuplicateEntityError
from domain.entities.user_entity import User
from domain.repositories.user_repository import UserRepository
from infrastructure.security.security_service import SecurityService

logger = logging.getLogger(__name__)


class RegisterCommand:
    """Command to register a new user in the system.

    This command validates the request, checks email uniqueness,
    hashes the password, creates the domain entity and persists it.

    Attributes:
        _user_repo: Repository for user persistence.
        _security_service: Service for password hashing.
    """

    def __init__(
        self,
        user_repo: UserRepository,
        security_service: SecurityService,
    ) -> None:
        """Initialize the command with required dependencies.

        Args:
            user_repo: Repository for user persistence.
            security_service: Service for password hashing.
        """

        self._user_repo = user_repo
        self._security_service = security_service

    async def execute(self, request: RegisterRequest) -> UserResponse:
        """Execute the user registration flow.

        Steps:
            1. Check if email is already taken.
            2. Hash the password.
            3. Create the domain entity.
            4. Persist the user.
            5. Return the response DTO.

        Args:
            request: Validated registration data.

        Returns:
            The created user as a response DTO.

        Raises:
            DuplicateEntityError: If the email is already registered.
        """

        logger.info(
            "Registering new user",
            extra={
                "extra_data": {
                    "email": request.email,
                    "role": request.role.value,
                }
            },
        )

        # Step 1: Check if email is already taken
        existing_user = await self._user_repo.get_by_email(request.email)

        if existing_user is not None:
            raise DuplicateEntityError(
                f"User with email {request.email} already exists"
            )

        # Step 2: Hash the password
        hashed_password = self._security_service.hash_password(request.password)

        # Step 3: Create the domain entity
        user = User.create(
            email=request.email,
            hashed_password=hashed_password,
            full_name=request.full_name,
            role=request.role,
            phone=request.phone,
        )

        # Step 4: Persist the user
        saved_user = await self._user_repo.save(user)

        logger.info(
            "User registered successfully",
            extra={
                "extra_data": {
                    "user_id": str(saved_user.id),
                    "email": saved_user.email,
                }
            },
        )

        # Step 5: Map domain entity to response DTO
        return UserResponse.model_validate(saved_user)
