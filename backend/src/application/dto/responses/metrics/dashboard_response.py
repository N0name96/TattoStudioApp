"""Metrics DTOs for analytics responses."""

from pydantic import BaseModel


class AgeSegmentData(BaseModel):
    range_18_25: int = 0
    range_26_35: int = 0
    range_36_45: int = 0
    range_46_55: int = 0
    range_55_plus: int = 0


class ClientSourceData(BaseModel):
    instagram: int = 0
    tiktok: int = 0
    recommendation: int = 0
    google_maps: int = 0
    walk_in: int = 0
    event: int = 0
    other: int = 0


class ArtistPerformanceData(BaseModel):
    artist_id: str
    artist_name: str
    completed_services: int = 0
    total_revenue: float = 0.0
    cancellation_rate: float = 0.0
    avg_rating: float = 0.0


class OverviewMetrics(BaseModel):
    total_appointments: int = 0
    completed_services: int = 0
    cancelled_services: int = 0
    total_revenue: float = 0.0
    avg_ticket: float = 0.0
    active_artists: int = 0
    active_clients: int = 0


class DashboardResponse(BaseModel):
    overview: OverviewMetrics
    age_segments: AgeSegmentData
    client_sources: ClientSourceData
    top_artists: list[ArtistPerformanceData]
