"""
Pydantic v2 schemas for Domain endpoints.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator
import re


def _clean_domain(domain: str) -> str:
    """Strip scheme and trailing slashes, lowercase."""
    domain = re.sub(r"^https?://", "", domain.strip().lower())
    domain = domain.rstrip("/")
    return domain


class DomainCreate(BaseModel):
    domain: str
    project_id: int
    display_name: Optional[str] = None
    is_primary: bool = False

    @field_validator("domain")
    @classmethod
    def clean_domain(cls, v: str) -> str:
        return _clean_domain(v)


class DomainResponse(BaseModel):
    id: int
    project_id: int
    domain: str
    display_name: Optional[str]
    is_primary: bool
    is_active: bool
    created_at: Optional[datetime]
    last_crawled_at: Optional[datetime]
    last_analyzed_at: Optional[datetime]

    model_config = {"from_attributes": True}
