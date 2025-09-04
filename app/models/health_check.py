from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"


class HealthCheck(BaseModel):
    status: HealthStatus
    timestamp: datetime
    version: str
    uptime_seconds: float
    # checks: List[ServiceCheck] = []
