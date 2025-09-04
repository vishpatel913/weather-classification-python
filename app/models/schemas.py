from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEGRADED = "degraded"


# class ServiceCheck(BaseModel):
#     name: str
#     status: HealthStatus
#     response_time_ms: Optional[float] = None
#     error: Optional[str] = None


class HealthCheck(BaseModel):
    status: HealthStatus
    timestamp: datetime
    version: str
    uptime_seconds: float
    # checks: List[ServiceCheck] = []


class ErrorResponse(BaseModel):
    error: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)
    request_id: Optional[str] = None
