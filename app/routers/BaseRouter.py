from fastapi import APIRouter
import time
import structlog
from datetime import datetime

from app.schemas.HealthCheck import HealthCheck
from app.config import settings

logger = structlog.get_logger()


BaseRouter = APIRouter()


@BaseRouter.get("/hello")
async def hello_world():
    """Test endpoint"""

    logger.info("Hello world requested")

    return {"Welcome": "Python FastAPI image running on Lambda"}


@BaseRouter.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint"""

    healthy_status = "healthy"

    logger.info("Health check requested", status=healthy_status)

    return HealthCheck(
        status=healthy_status,
        timestamp=datetime.now(),
        version=settings.app_version
    )

    # # Return appropriate HTTP status based on health
    # if health_data.status == "unhealthy":
    #     raise HTTPException(
    #         status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
    #         detail=health_data.dict()
    #     )

    # return health_data
