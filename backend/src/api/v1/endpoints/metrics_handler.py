"""API handler for metrics/analytics endpoints (admin only).

Endpoints:
    GET /metrics/dashboard - Dashboard overview (admin)
"""

import logging

from fastapi import APIRouter, Depends

from api.deps import require_role
from application.dto.responses.metrics.dashboard_response import DashboardResponse
from application.use_cases.metrics.metrics_use_case import MetricsUseCase
from core.container import container
from core.responses import SuccessResponse
from domain.entities.user_entity import User
from domain.enums.user_role import UserRole

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/metrics", tags=["metrics"])


def get_metrics_use_case() -> MetricsUseCase:
    return MetricsUseCase(
        appointment_repo=container.appointment_repository,
        artist_repo=container.artist_repository,
        client_repo=container.client_repository,
    )


@router.get("/dashboard", response_model=SuccessResponse[DashboardResponse])
async def get_dashboard(
    use_case: MetricsUseCase = Depends(get_metrics_use_case),
    current_user: User = Depends(require_role(UserRole.ADMIN)),
) -> SuccessResponse[DashboardResponse]:
    dashboard = await use_case.get_dashboard()
    return SuccessResponse(data=dashboard)
