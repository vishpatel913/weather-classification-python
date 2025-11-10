"""Schema definitions for health check responses."""

from enum import Enum
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class HealthStatus(str, Enum):
    """Enum of possible health statuses."""

    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"


class HealthCheck(BaseModel):
    """Schema for health check response."""

    status: HealthStatus
    timestamp: datetime
    version: str
    uptime_seconds: Optional[float] = 0.0
    # checks: List[ServiceCheck] = []
