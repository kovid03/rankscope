"""
Abstract Base Class for SERP Providers
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from app.models.models import DeviceType, PositionType, SerpProvider


class SerpItem(BaseModel):
    position: int
    url: str
    domain: str
    title: Optional[str] = None
    description: Optional[str] = None
    position_type: PositionType = PositionType.organic
    is_featured_snippet: bool = False
    breadcrumb: Optional[str] = None


class SerpResponse(BaseModel):
    keyword: str
    country_code: str
    language_code: str
    device: DeviceType
    provider: SerpProvider
    result_depth: int
    items: List[SerpItem]
    target_rankings: List[SerpItem] = []
    best_position: Optional[int] = None
    raw_response: Optional[Dict[str, Any]] = None
    cost_usd: Optional[float] = 0.0


class BaseSerpProvider(ABC):
    @abstractmethod
    def check_ranking(
        self,
        keyword: str,
        country: str,
        language: str,
        device: DeviceType,
        target_domain: Optional[str] = None,
        result_depth: int = 100,
        city: Optional[str] = None,
    ) -> SerpResponse:
        """
        Execute SERP check for a keyword and optionally identify target_domain's ranking.
        """
        pass
