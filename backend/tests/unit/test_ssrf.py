import pytest
from app.core.ssrf_protection import validate_url, _is_ip_blocked


def test_blocked_ips():
    assert _is_ip_blocked("127.0.0.1") is True
    assert _is_ip_blocked("10.0.0.1") is True
    assert _is_ip_blocked("192.168.1.1") is True
    assert _is_ip_blocked("172.16.0.1") is True
    assert _is_ip_blocked("169.254.169.254") is True
    assert _is_ip_blocked("::1") is True
    assert _is_ip_blocked("8.8.8.8") is False
    assert _is_ip_blocked("1.1.1.1") is False


def test_validate_url_schemes():
    with pytest.raises(ValueError, match="Disallowed scheme"):
        validate_url("ftp://example.com")
    with pytest.raises(ValueError, match="Disallowed scheme"):
        validate_url("file:///etc/passwd")


def test_validate_url_direct_ip():
    with pytest.raises(ValueError, match="blocked range"):
        validate_url("http://127.0.0.1:8000/api")
    with pytest.raises(ValueError, match="blocked range"):
        validate_url("http://192.168.0.1/")
