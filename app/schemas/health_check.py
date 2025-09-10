from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"


class HealthCheck(BaseModel):
    status: HealthStatus
    timestamp: datetime
    version: str
    uptime_seconds: Optional[float] = 0.0
    # checks: List[ServiceCheck] = []
