"""Query to compute dashboard metrics from aggregated data."""

import logging
from application.dto.responses.metrics.dashboard_response import (
    AgeSegmentData,
    ArtistPerformanceData,
    ClientSourceData,
    DashboardResponse,
    OverviewMetrics,
)
from domain.enums.appointment_status import AppointmentStatus
from domain.repositories.appointment_repository import AppointmentRepository
from domain.repositories.artist_repository import ArtistRepository
from domain.repositories.client_repository import ClientRepository

logger = logging.getLogger(__name__)


class GetDashboardMetricsQuery:
    def __init__(
        self,
        appointment_repo: AppointmentRepository,
        artist_repo: ArtistRepository,
        client_repo: ClientRepository,
    ) -> None:
        self._appointment_repo = appointment_repo
        self._artist_repo = artist_repo
        self._client_repo = client_repo

    async def execute(self) -> DashboardResponse:
        appointments = await self._appointment_repo.list_all()
        artists = await self._artist_repo.get_all(active_only=False)
        clients = await self._client_repo.list_all(active_only=False)

        completed = [a for a in appointments if a.status == AppointmentStatus.COMPLETED]
        cancelled = [a for a in appointments if a.status == AppointmentStatus.CANCELLED]
        no_shows = [a for a in appointments if a.status == AppointmentStatus.NO_SHOW]

        total_revenue = sum(a.total_price for a in completed)
        active_artists = sum(1 for a in artists if a.is_active)

        overview = OverviewMetrics(
            total_appointments=len(appointments),
            completed_services=len(completed),
            cancelled_services=len(cancelled) + len(no_shows),
            total_revenue=total_revenue,
            avg_ticket=total_revenue / len(completed) if completed else 0.0,
            active_artists=active_artists,
            active_clients=sum(1 for c in clients if c.is_active),
        )

        age_segments = _compute_age_segments(clients)
        client_sources = _compute_client_sources(clients)
        top_artists = _compute_artist_performance(appointments, artists)

        return DashboardResponse(
            overview=overview,
            age_segments=age_segments,
            client_sources=client_sources,
            top_artists=top_artists,
        )


def _compute_age_segments(clients) -> AgeSegmentData:
    from datetime import date
    today = date.today()
    segments = AgeSegmentData()

    for client in clients:
        if not client.birth_date:
            continue
        age = today.year - client.birth_date.year
        if (today.month, today.day) < (client.birth_date.month, client.birth_date.day):
            age -= 1

        if age <= 25:
            segments.range_18_25 += 1
        elif age <= 35:
            segments.range_26_35 += 1
        elif age <= 45:
            segments.range_36_45 += 1
        elif age <= 55:
            segments.range_46_55 += 1
        else:
            segments.range_55_plus += 1

    return segments


def _compute_client_sources(clients) -> ClientSourceData:
    sources = ClientSourceData()

    for client in clients:
        if not client.source:
            sources.other += 1
        elif client.source.value == "instagram":
            sources.instagram += 1
        elif client.source.value == "tiktok":
            sources.tiktok += 1
        elif client.source.value == "recommendation":
            sources.recommendation += 1
        elif client.source.value == "google_maps":
            sources.google_maps += 1
        elif client.source.value == "walk_in":
            sources.walk_in += 1
        elif client.source.value == "event":
            sources.event += 1
        else:
            sources.other += 1

    return sources


def _compute_artist_performance(appointments, artists) -> list[ArtistPerformanceData]:
    from domain.enums.appointment_status import AppointmentStatus

    artist_map = {a.id: a for a in artists}
    result = []

    for artist in artists:
        artist_appts = [a for a in appointments if a.artist_id == artist.id]
        completed_services = [a for a in artist_appts if a.status == AppointmentStatus.COMPLETED]
        cancelled_services = [a for a in artist_appts if a.status in (AppointmentStatus.CANCELLED, AppointmentStatus.NO_SHOW)]

        total = len(artist_appts)
        perf = ArtistPerformanceData(
            artist_id=str(artist.id),
            artist_name=artist.name,
            completed_services=len(completed_services),
            total_revenue=sum(a.total_price for a in completed_services),
            cancellation_rate=len(cancelled_services) / total if total > 0 else 0.0,
            avg_rating=0.0,
        )

        result.append(perf)

    return result
