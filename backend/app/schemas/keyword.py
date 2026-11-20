"""
Pydantic v2 schemas for Keyword and SERP check endpoints.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class KeywordCreate(BaseModel):
    keyword_text: str
    country_code: str = "IN"
    language_code: str = "en"


class KeywordResponse(BaseModel):
    id: int
    keyword_text: str
    country_code: str
    language_code: str
    created_at: Optional[datetime]

    model_config = {"from_attributes": True}


class SerpCheckRequest(BaseModel):
    keyword: str
    country: str = "IN"
    language: str = "en"
    device: str = "desktop"
    target_domain: str
    result_depth: int = 100
