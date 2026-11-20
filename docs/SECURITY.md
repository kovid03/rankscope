# RankScope — Security & SSRF Protection Policy

Security is a foundational pillar of RankScope. Because the platform crawls arbitrary third-party domains submitted by users, strict boundaries and defensive architecture are enforced.

---

## 1. Server-Side Request Forgery (SSRF) Defense

The crawler implements active multi-layer SSRF safeguards:
1. **Scheme Whitelisting:** Only `http` and `https` schemes are accepted. Protocols like `file://`, `ftp://`, `gopher://`, `dict://` are strictly rejected.
2. **IP Range Blocklist:**
   - IPv4: Private address blocks (RFC 1918: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`)
   - Loopback: `127.0.0.0/8`
   - Link-local & Cloud Metadata: `169.254.0.0/16` (including `169.254.169.254` AWS metadata)
   - Carrier-grade NAT: `100.64.0.0/10`
   - IPv6: Loopback `::1/128`, Unique Local `fc00::/7`, Link-local `fe80::/10`
3. **Pre-Flight DNS Resolution:** Hostnames are resolved through DNS and checked against the IP blocklist prior to initiating network connections.
4. **Redirect Validation:** Every HTTP redirect destination is individually validated through the SSRF guard before following.

---

## 2. Authentication & Data Isolation

- **Password Hashing:** Passwords are salted and hashed using raw `bcrypt` with work factor 12. Input strings are constrained to 72 bytes to avoid truncation edge cases.
- **JWT Protection:** Signed using HMAC-SHA256 with user ID claims (`sub`) and expiration timestamps.
- **Multi-Tenant Ownership:** Every database record query enforces `user_id` filtering, preventing cross-tenant access.
