import pytest
from app.models.models import DeviceType, SerpProvider
from app.services.serp.mock import MockSerpProvider


def test_mock_serp_provider():
    provider = MockSerpProvider()
    response = provider.check_ranking(
        keyword="best python course",
        country="IN",
        language="en",
        device=DeviceType.desktop,
        target_domain="github.com",
        result_depth=20,
    )

    assert response.provider == SerpProvider.mock
    assert response.keyword == "best python course"
    assert len(response.items) == 20
    assert response.country_code == "IN"
    assert response.cost_usd == 0.0
