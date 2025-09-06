from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class ErrorResponse(BaseModel):
    error: str
    message: str
    timestamp: datetime = Field(default_factory=datetime.now)
    request_id: Optional[str] = None
