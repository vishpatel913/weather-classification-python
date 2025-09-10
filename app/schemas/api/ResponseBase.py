from pydantic import BaseModel, Field
from datetime import datetime

# from typing import Optional


class ResponseBase(BaseModel):
    # request_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.now)


class ErrorResponse(ResponseBase):
    message: str
    error: str
