import time
import structlog
from datetime import datetime

from app.models.health_check import HealthCheck
from app.config import settings

logger = structlog.get_logger()

# Global startup time for uptime calculation
startup_time = time.time()


async def get_health_check() -> HealthCheck:
    """Comprehensive health check"""

    uptime = time.time() - startup_time

    return HealthCheck(
        status="healthy",
        timestamp=datetime.now(),
        version=settings.app_version,
        uptime_seconds=round(uptime, 2),
    )
