"""Schema definitions for API response base."""

from datetime import datetime
from pydantic import BaseModel, Field

# from typing import Optional


class ResponseBase(BaseModel):
    """Base schema for API responses."""

    # request_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class ErrorResponse(ResponseBase):
    """Schema for error responses."""

    message: str
    error: str
