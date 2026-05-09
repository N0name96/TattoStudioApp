"""Use case for metrics operations."""

from application.dto.responses.metrics.dashboard_response import DashboardResponse
from application.queries.metrics.get_dashboard_metrics_query import GetDashboardMetricsQuery
from domain.repositories.appointment_repository import AppointmentRepository
from domain.repositories.artist_repository import ArtistRepository
from domain.repositories.client_repository import ClientRepository


class MetricsUseCase:
    def __init__(
        self,
        appointment_repo: AppointmentRepository,
        artist_repo: ArtistRepository,
        client_repo: ClientRepository,
    ) -> None:
        self._dashboard_query = GetDashboardMetricsQuery(
            appointment_repo, artist_repo, client_repo
        )

    async def get_dashboard(self) -> DashboardResponse:
        return await self._dashboard_query.execute()
