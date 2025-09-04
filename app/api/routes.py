import structlog
from fastapi import APIRouter, HTTPException, Depends, status

from app.models.schemas import (
    HealthCheck,
)
from app.api.dependencies import get_health_check

logger = structlog.get_logger()
router = APIRouter()


@router.get("/health", response_model=HealthCheck)
async def health_check(health_data: HealthCheck = Depends(get_health_check)):
    """Comprehensive health check endpoint"""

    logger.info("Health check requested", status=health_data.status.value)

    # Return appropriate HTTP status based on health
    if health_data.status == "unhealthy":
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=health_data.dict()
        )

    return health_data
