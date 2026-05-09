"""API handler for notification endpoints.

Endpoints:
    POST   /notifications              - Create notification (admin)
    GET    /notifications/{id}          - Get notification detail
    GET    /notifications               - List notifications (user)
    PUT    /notifications/{id}/read     - Mark as read
    PUT    /notifications/read-all      - Mark all as read
    POST   /notifications/{id}/send     - Send notification (admin)
"""

import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from api.deps import get_current_active_user, require_role
from application.dto.requests.notifications.create_notification_request import (
    CreateNotificationRequest,
)
from application.dto.responses.notifications.notification_response import (
    NotificationResponse,
)
from application.use_cases.notifications.notification_use_case import (
    NotificationUseCase,
)
from core.container import container
from core.errors import BusinessRuleError, EntityNotFoundError
from core.responses import SuccessResponse
from domain.entities.user_entity import User
from domain.enums.user_role import UserRole

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/notifications", tags=["notifications"])


def get_notification_use_case() -> NotificationUseCase:
    return NotificationUseCase(
        notification_repo=container.notification_repository,
        user_repo=container.user_repository,
    )


@router.post("/", response_model=SuccessResponse[NotificationResponse], status_code=status.HTTP_201_CREATED)
async def create_notification(
    request: CreateNotificationRequest,
    use_case: NotificationUseCase = Depends(get_notification_use_case),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
) -> SuccessResponse[NotificationResponse]:
    try:
        notification = await use_case.create_notification(request)
        return SuccessResponse(data=notification, message="Notification created")
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    except BusinessRuleError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message) from e


@router.get("/{notification_id}", response_model=SuccessResponse[NotificationResponse])
async def get_notification(
    notification_id: UUID,
    use_case: NotificationUseCase = Depends(get_notification_use_case),
    current_user: User = Depends(get_current_active_user),
) -> SuccessResponse[NotificationResponse]:
    try:
        notification = await use_case.get_notification(notification_id)
        return SuccessResponse(data=notification)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e


@router.get("/", response_model=SuccessResponse[list[NotificationResponse]])
async def list_notifications(
    use_case: NotificationUseCase = Depends(get_notification_use_case),
    current_user: User = Depends(get_current_active_user),
) -> SuccessResponse[list[NotificationResponse]]:
    notifications = await use_case.list_notifications(user_id=current_user.id)
    return SuccessResponse(data=notifications)


@router.put("/{notification_id}/read", response_model=SuccessResponse[NotificationResponse])
async def mark_read(
    notification_id: UUID,
    use_case: NotificationUseCase = Depends(get_notification_use_case),
    current_user: User = Depends(get_current_active_user),
) -> SuccessResponse[NotificationResponse]:
    try:
        notification = await use_case.mark_read(notification_id)
        return SuccessResponse(data=notification)
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e


@router.put("/read-all", response_model=SuccessResponse[list[NotificationResponse]])
async def mark_all_read(
    use_case: NotificationUseCase = Depends(get_notification_use_case),
    current_user: User = Depends(get_current_active_user),
) -> SuccessResponse[list[NotificationResponse]]:
    notifications = await use_case.mark_all_read(current_user.id)
    return SuccessResponse(data=notifications, message="All notifications marked as read")


@router.post("/{notification_id}/send", response_model=SuccessResponse[NotificationResponse])
async def send_notification(
    notification_id: UUID,
    use_case: NotificationUseCase = Depends(get_notification_use_case),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
) -> SuccessResponse[NotificationResponse]:
    try:
        notification = await use_case.mark_sent(notification_id)
        return SuccessResponse(data=notification, message="Notification sent")
    except EntityNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=e.message) from e
    except BusinessRuleError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.message) from e
