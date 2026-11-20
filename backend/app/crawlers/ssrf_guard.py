"""
SSRF Guard for Crawlers and HTTP Clients
"""
from typing import Optional
from app.core.ssrf_protection import validate_url, _is_ip_blocked


class SSRFValidationError(ValueError):
    """Raised when URL validation fails SSRF checks."""
    pass


def ensure_safe_url(url: str) -> str:
    """
    Validates URL scheme and resolves target hostname to ensure no private/loopback/internal
    IP addresses are targeted.
    """
    try:
        return validate_url(url)
    except ValueError as e:
        raise SSRFValidationError(str(e)) from e
