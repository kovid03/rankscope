"""
SSRF protection — validates URLs before the crawler fetches them.
Rejects private, loopback, link-local, and reserved IP ranges.
"""
import ipaddress
import socket
from typing import List
from urllib.parse import urlparse

_BLOCKED_V4: List[ipaddress.IPv4Network] = [
    ipaddress.IPv4Network("0.0.0.0/8"),
    ipaddress.IPv4Network("10.0.0.0/8"),
    ipaddress.IPv4Network("100.64.0.0/10"),
    ipaddress.IPv4Network("127.0.0.0/8"),
    ipaddress.IPv4Network("169.254.0.0/16"),
    ipaddress.IPv4Network("172.16.0.0/12"),
    ipaddress.IPv4Network("192.0.0.0/24"),
    ipaddress.IPv4Network("192.168.0.0/16"),
    ipaddress.IPv4Network("198.18.0.0/15"),
    ipaddress.IPv4Network("198.51.100.0/24"),
    ipaddress.IPv4Network("203.0.113.0/24"),
    ipaddress.IPv4Network("224.0.0.0/4"),
    ipaddress.IPv4Network("240.0.0.0/4"),
]

_BLOCKED_V6: List[ipaddress.IPv6Network] = [
    ipaddress.IPv6Network("::1/128"),
    ipaddress.IPv6Network("fc00::/7"),
    ipaddress.IPv6Network("fe80::/10"),
    ipaddress.IPv6Network("::/128"),
]


def _is_ip_blocked(ip_str: str) -> bool:
    try:
        addr = ipaddress.ip_address(ip_str)
        if isinstance(addr, ipaddress.IPv4Address):
            return any(addr in net for net in _BLOCKED_V4)
        return any(addr in net for net in _BLOCKED_V6)
    except ValueError:
        return True


def validate_url(url: str) -> str:
    """
    Validate a URL is safe for crawler use.
    Raises ValueError if scheme is bad, hostname is private/reserved, or DNS fails.
    Returns the URL unchanged if safe.
    """
    parsed = urlparse(url)
    if parsed.scheme not in ("http", "https"):
        raise ValueError(f"Disallowed scheme '{parsed.scheme}'. Only http/https allowed.")

    hostname = parsed.hostname
    if not hostname:
        raise ValueError("URL has no hostname.")

    # Direct IP check
    try:
        direct = ipaddress.ip_address(hostname)
        if _is_ip_blocked(str(direct)):
            raise ValueError(f"IP '{hostname}' is in a blocked range (SSRF protection).")
        return url
    except ValueError as exc:
        if "blocked range" in str(exc):
            raise
        # Domain name — fall through to DNS

    # DNS resolution
    try:
        results = socket.getaddrinfo(hostname, None)
    except socket.gaierror as exc:
        raise ValueError(f"DNS resolution failed for '{hostname}': {exc}") from exc

    for result in results:
        ip = result[4][0]
        if _is_ip_blocked(ip):
            raise ValueError(
                f"Hostname '{hostname}' resolves to blocked IP '{ip}' (SSRF protection)."
            )
    return url
