"""
Mock SERP Provider for testing and local development without incurring API costs.
"""
from typing import Optional, List
import hashlib
from app.models.models import DeviceType, PositionType, SerpProvider
from app.services.serp.base import BaseSerpProvider, SerpItem, SerpResponse


class MockSerpProvider(BaseSerpProvider):
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
        # Generate pseudo-deterministic SERP based on keyword hash
        h = int(hashlib.md5(keyword.encode("utf-8")).hexdigest(), 16)
        
        items: List[SerpItem] = []
        popular_domains = [
            "wikipedia.org",
            "amazon.in",
            "youtube.com",
            "quora.com",
            "reddit.com",
            "nytimes.com",
            "medium.com",
            "github.com",
            "linkedin.com",
            "forbes.com"
        ]

        target_rankings: List[SerpItem] = []
        best_pos = None

        # Determine if target domain will be placed in top 100
        target_in_top = target_domain and ((h % 10) > 2) # 70% chance to rank
        target_slot = (h % 30) + 1 if target_in_top else None

        for pos in range(1, min(result_depth + 1, 101)):
            if pos == target_slot and target_domain:
                domain = target_domain
                url = f"https://{target_domain}/article-{keyword.replace(' ', '-')}"
                title = f"{keyword.title()} - Official {target_domain}"
                item = SerpItem(
                    position=pos,
                    url=url,
                    domain=domain,
                    title=title,
                    description=f"Top ranking page for {keyword} on {target_domain}.",
                    position_type=PositionType.organic,
                )
                items.append(item)
                target_rankings.append(item)
                if best_pos is None or pos < best_pos:
                    best_pos = pos
            else:
                domain = popular_domains[(pos + (h % 7)) % len(popular_domains)]
                url = f"https://www.{domain}/topic/{keyword.replace(' ', '-')}"
                title = f"{keyword.title()} | {domain}"
                item = SerpItem(
                    position=pos,
                    url=url,
                    domain=domain,
                    title=title,
                    description=f"Information regarding {keyword} published on {domain}.",
                    position_type=PositionType.organic,
                    is_featured_snippet=(pos == 1 and (h % 5 == 0)),
                )
                items.append(item)

        return SerpResponse(
            keyword=keyword,
            country_code=country,
            language_code=language,
            device=device,
            provider=SerpProvider.mock,
            result_depth=result_depth,
            items=items,
            target_rankings=target_rankings,
            best_position=best_pos,
            raw_response={"mock": True, "seed": h},
            cost_usd=0.0,
        )
