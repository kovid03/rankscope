"""
Pydantic v2 schemas for ranking position and history endpoints.
"""
from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel


class RankingPositionResponse(BaseModel):
    id: int
    domain_id: int
    keyword_id: int
    ranking_url: Optional[str]
    position: Optional[int]
    best_position: Optional[int]
    position_type: str
    country_code: str
    language_code: str
    device: str
    provider: str
    observed_at: Optional[datetime]

    model_config = {"from_attributes": True}


class RankingHistoryResponse(BaseModel):
    id: int
    domain_id: int
    keyword_id: int
    observed_date: date
    position: Optional[int]
    ranking_url: Optional[str]
    position_type: str
    country_code: str
    device: str
    provider: str
    created_at: Optional[datetime]

    model_config = {"from_attributes": True}
