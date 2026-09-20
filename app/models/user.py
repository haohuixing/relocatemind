from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class UserSession(BaseModel):
    id: str
    email: str = Field(..., min_length=3, max_length=320)
    created_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)