"""Main application entry point for the FastAPI service."""

from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from mangum import Mangum

from app.routers.base_router import BaseRouter
from app.routers.v1.weather_router import WeatherRouter
from app.config import settings


@asynccontextmanager
async def lifespan():
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    print(f"Starting {settings.app_name} v{settings.app_version}")
    # Future: Initialize ML models, database connections, etc.

    yield

    # Shutdown
    print("Shutting down...")
    # Future: Cleanup resources


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Weather-based clothing recommendation service",
    lifespan=lifespan,
    root_path="/dev",  # Config API Gateway
)

# CORS middleware for frontend integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(WeatherRouter, prefix="/api")
app.include_router(BaseRouter, prefix="/api")

handler = Mangum(app, lifespan="off", api_gateway_base_path="/dev")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app", host="0.0.0.0", port=8080, reload=True, log_level="info"
    )
