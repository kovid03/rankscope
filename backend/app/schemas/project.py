"""
Pydantic v2 schemas for Project endpoints.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class ProjectResponse(BaseModel):
    id: int
    user_id: int
    name: str
    description: Optional[str]
    is_active: bool
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = {"from_attributes": True}
