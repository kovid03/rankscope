"""
RankScope — All 20 Database Models
Normalized PostgreSQL schema designed for historical analysis and efficient querying.
"""
import enum
from datetime import datetime, date
from typing import Optional
from sqlalchemy import (
    Column, Integer, String, Boolean, DateTime, Date, Float,
    Text, ForeignKey, Enum, JSON, BigInteger, UniqueConstraint, Index
)
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base


# ── Enums ─────────────────────────────────────────────────────────────────────

class DeviceType(str, enum.Enum):
    desktop = "desktop"
    mobile = "mobile"
    tablet = "tablet"

class PositionType(str, enum.Enum):
    organic = "organic"
    paid = "paid"
    featured_snippet = "featured_snippet"
    local_pack = "local_pack"
    image = "image"
    video = "video"

class CrawlStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"
    cancelled = "cancelled"

class KeywordClassification(str, enum.Enum):
    discovered = "discovered"
    candidate = "candidate"
    verified_ranking = "verified_ranking"
    historical_ranking = "historical_ranking"
    competitor_only = "competitor_only"

class CheckFrequency(str, enum.Enum):
    manual = "manual"
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"

class AuditSeverity(str, enum.Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"
    info = "info"

class JobStatus(str, enum.Enum):
    pending = "pending"
    running = "running"
    completed = "completed"
    failed = "failed"

class SerpProvider(str, enum.Enum):
    dataforseo = "dataforseo"
    serpapi = "serpapi"
    mock = "mock"


# ── 1. users ──────────────────────────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")


# ── 2. projects ───────────────────────────────────────────────────────────────

class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="projects")
    domains = relationship("Domain", back_populates="project", cascade="all, delete-orphan")


# ── 3. domains ────────────────────────────────────────────────────────────────

class Domain(Base):
    __tablename__ = "domains"
    __table_args__ = (
        UniqueConstraint("project_id", "domain", name="uq_project_domain"),
    )

    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True)
    domain = Column(String(255), nullable=False, index=True)
    display_name = Column(String(200), nullable=True)
    is_primary = Column(Boolean, default=False)       # the target domain vs competitors
    is_active = Column(Boolean, default=True)
    last_crawled_at = Column(DateTime(timezone=True), nullable=True)
    last_analyzed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    project = relationship("Project", back_populates="domains")
    competitors = relationship("Competitor", foreign_keys="[Competitor.target_domain_id]", back_populates="target_domain")
    crawl_jobs = relationship("CrawlJob", back_populates="domain", cascade="all, delete-orphan")
    crawled_pages = relationship("CrawledPage", back_populates="domain", cascade="all, delete-orphan")
    ranking_positions = relationship("RankingPosition", back_populates="domain", cascade="all, delete-orphan")
    seo_audits = relationship("SeoAudit", back_populates="domain", cascade="all, delete-orphan")
    traffic_estimates = relationship("TrafficEstimate", back_populates="domain", cascade="all, delete-orphan")
    backlinks = relationship("Backlink", back_populates="target_domain", cascade="all, delete-orphan")


# ── 4. competitors ────────────────────────────────────────────────────────────

class Competitor(Base):
    __tablename__ = "competitors"
    __table_args__ = (
        UniqueConstraint("target_domain_id", "competitor_domain", name="uq_target_competitor"),
    )

    id = Column(Integer, primary_key=True, index=True)
    target_domain_id = Column(Integer, ForeignKey("domains.id", ondelete="CASCADE"), nullable=False, index=True)
    competitor_domain = Column(String(255), nullable=False, index=True)
    display_name = Column(String(200), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    target_domain = relationship("Domain", foreign_keys=[target_domain_id], back_populates="competitors")


# ── 5. crawled_pages ─────────────────────────────────────────────────────────

class CrawledPage(Base):
    __tablename__ = "crawled_pages"
    __table_args__ = (
        Index("ix_crawled_pages_domain_url", "domain_id", "url"),
    )

    id = Column(Integer, primary_key=True, index=True)
    domain_id = Column(Integer, ForeignKey("domains.id", ondelete="CASCADE"), nullable=False, index=True)
    crawl_job_id = Column(Integer, ForeignKey("crawl_jobs.id", ondelete="SET NULL"), nullable=True)
    url = Column(Text, nullable=False)
    canonical_url = Column(Text, nullable=True)
    http_status = Column(Integer, nullable=True)
    page_title = Column(Text, nullable=True)
    meta_description = Column(Text, nullable=True)
    h1 = Column(Text, nullable=True)
    h2_list = Column(JSON, nullable=True)       # list of h2 strings
    h3_list = Column(JSON, nullable=True)       # list of h3 strings
    main_content = Column(Text, nullable=True)
    robots_directives = Column(String(200), nullable=True)
    canonical_self = Column(Boolean, nullable=True)
    is_indexable = Column(Boolean, nullable=True)
    language = Column(String(20), nullable=True)
    page_size_bytes = Column(Integer, nullable=True)
    response_time_ms = Column(Integer, nullable=True)
    internal_links = Column(JSON, nullable=True)   # list of urls
    external_links = Column(JSON, nullable=True)   # list of urls
    image_alts = Column(JSON, nullable=True)       # {src: alt}
    structured_data = Column(JSON, nullable=True)
    crawled_at = Column(DateTime(timezone=True), server_default=func.now())

    domain = relationship("Domain", back_populates="crawled_pages")
    crawl_job = relationship("CrawlJob", back_populates="pages")


# ── 6. crawl_jobs ─────────────────────────────────────────────────────────────

class CrawlJob(Base):
    __tablename__ = "crawl_jobs"

    id = Column(Integer, primary_key=True, index=True)
    domain_id = Column(Integer, ForeignKey("domains.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(Enum(CrawlStatus), default=CrawlStatus.pending, nullable=False, index=True)
    pages_discovered = Column(Integer, default=0)
    pages_crawled = Column(Integer, default=0)
    pages_failed = Column(Integer, default=0)
    max_pages = Column(Integer, default=200)
    max_depth = Column(Integer, default=5)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    domain = relationship("Domain", back_populates="crawl_jobs")
    pages = relationship("CrawledPage", back_populates="crawl_job")


# ── 7. keywords ───────────────────────────────────────────────────────────────

class Keyword(Base):
    __tablename__ = "keywords"
    __table_args__ = (
        UniqueConstraint("keyword_text", "country_code", "language_code", name="uq_keyword_locale"),
    )

    id = Column(Integer, primary_key=True, index=True)
    keyword_text = Column(String(500), nullable=False, index=True)
    country_code = Column(String(10), default="IN", nullable=False)
    language_code = Column(String(10), default="en", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    metrics = relationship("KeywordMetrics", back_populates="keyword", cascade="all, delete-orphan")
    sources = relationship("KeywordSource", back_populates="keyword", cascade="all, delete-orphan")
    serp_snapshots = relationship("SerpSnapshot", back_populates="keyword", cascade="all, delete-orphan")
    ranking_positions = relationship("RankingPosition", back_populates="keyword", cascade="all, delete-orphan")
    traffic_estimates = relationship("TrafficEstimate", back_populates="keyword", cascade="all, delete-orphan")


# ── 8. keyword_metrics ────────────────────────────────────────────────────────

class KeywordMetrics(Base):
    __tablename__ = "keyword_metrics"

    id = Column(Integer, primary_key=True, index=True)
    keyword_id = Column(Integer, ForeignKey("keywords.id", ondelete="CASCADE"), nullable=False, index=True)
    search_volume = Column(Integer, nullable=True)
    keyword_difficulty = Column(Float, nullable=True)    # 0-100
    cpc_usd = Column(Float, nullable=True)
    competition = Column(Float, nullable=True)           # 0-1
    trend_data = Column(JSON, nullable=True)             # monthly volumes for last 12 months
    provider = Column(String(50), nullable=True)         # e.g. "dataforseo"
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())

    keyword = relationship("Keyword", back_populates="metrics")


# ── 9. keyword_sources ────────────────────────────────────────────────────────

class KeywordSource(Base):
    __tablename__ = "keyword_sources"

    id = Column(Integer, primary_key=True, index=True)
    keyword_id = Column(Integer, ForeignKey("keywords.id", ondelete="CASCADE"), nullable=False, index=True)
    domain_id = Column(Integer, ForeignKey("domains.id", ondelete="CASCADE"), nullable=True, index=True)
    classification = Column(Enum(KeywordClassification), nullable=False, index=True)
    source_type = Column(String(50), nullable=True)   # "page_title", "serp_analysis", "provider"
    source_url = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    keyword = relationship("Keyword", back_populates="sources")


# ── 10. serp_snapshots ────────────────────────────────────────────────────────

class SerpSnapshot(Base):
    __tablename__ = "serp_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    keyword_id = Column(Integer, ForeignKey("keywords.id", ondelete="CASCADE"), nullable=False, index=True)
    country_code = Column(String(10), default="IN", nullable=False)
    city = Column(String(100), nullable=True)
    language_code = Column(String(10), default="en", nullable=False)
    device = Column(Enum(DeviceType), default=DeviceType.desktop, nullable=False)
    result_depth = Column(Integer, default=100)
    provider = Column(Enum(SerpProvider), nullable=False)
    raw_response = Column(JSON, nullable=True)       # full provider response (optional)
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())
    cost_usd = Column(Float, nullable=True)          # cost of this API call

    keyword = relationship("Keyword", back_populates="serp_snapshots")
    results = relationship("SerpResult", back_populates="snapshot", cascade="all, delete-orphan")
    ranking_positions = relationship("RankingPosition", back_populates="snapshot")


# ── 11. serp_results ──────────────────────────────────────────────────────────

class SerpResult(Base):
    __tablename__ = "serp_results"

    id = Column(Integer, primary_key=True, index=True)
    snapshot_id = Column(Integer, ForeignKey("serp_snapshots.id", ondelete="CASCADE"), nullable=False, index=True)
    position = Column(Integer, nullable=False)
    url = Column(Text, nullable=False)
    domain = Column(String(255), nullable=False, index=True)
    title = Column(Text, nullable=True)
    description = Column(Text, nullable=True)
    position_type = Column(Enum(PositionType), default=PositionType.organic, nullable=False)
    breadcrumb = Column(Text, nullable=True)
    is_featured_snippet = Column(Boolean, default=False)

    snapshot = relationship("SerpSnapshot", back_populates="results")


# ── 12. ranking_positions ─────────────────────────────────────────────────────

class RankingPosition(Base):
    __tablename__ = "ranking_positions"
    __table_args__ = (
        Index("ix_ranking_positions_domain_keyword", "domain_id", "keyword_id"),
    )

    id = Column(Integer, primary_key=True, index=True)
    domain_id = Column(Integer, ForeignKey("domains.id", ondelete="CASCADE"), nullable=False, index=True)
    keyword_id = Column(Integer, ForeignKey("keywords.id", ondelete="CASCADE"), nullable=False, index=True)
    snapshot_id = Column(Integer, ForeignKey("serp_snapshots.id", ondelete="SET NULL"), nullable=True)
    ranking_url = Column(Text, nullable=True)
    position = Column(Integer, nullable=True)         # NULL = not found in depth
    best_position = Column(Integer, nullable=True)    # if multiple URLs rank
    position_type = Column(Enum(PositionType), default=PositionType.organic)
    country_code = Column(String(10), nullable=False)
    city = Column(String(100), nullable=True)
    language_code = Column(String(10), nullable=False)
    device = Column(Enum(DeviceType), nullable=False)
    result_depth_checked = Column(Integer, default=100)
    provider = Column(Enum(SerpProvider), nullable=False)
    observed_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    domain = relationship("Domain", back_populates="ranking_positions")
    keyword = relationship("Keyword", back_populates="ranking_positions")
    snapshot = relationship("SerpSnapshot", back_populates="ranking_positions")


# ── 13. ranking_history ───────────────────────────────────────────────────────

class RankingHistory(Base):
    """Immutable record — never updated, only appended."""
    __tablename__ = "ranking_history"
    __table_args__ = (
        Index("ix_ranking_history_domain_keyword_date", "domain_id", "keyword_id", "observed_date"),
    )

    id = Column(BigInteger, primary_key=True, index=True)
    domain_id = Column(Integer, ForeignKey("domains.id", ondelete="CASCADE"), nullable=False, index=True)
    keyword_id = Column(Integer, ForeignKey("keywords.id", ondelete="CASCADE"), nullable=False, index=True)
    observed_date = Column(Date, nullable=False, index=True)
    position = Column(Integer, nullable=True)
    ranking_url = Column(Text, nullable=True)
    position_type = Column(Enum(PositionType), default=PositionType.organic)
    country_code = Column(String(10), nullable=False)
    device = Column(Enum(DeviceType), nullable=False)
    provider = Column(Enum(SerpProvider), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ── 14. backlinks ─────────────────────────────────────────────────────────────

class Backlink(Base):
    __tablename__ = "backlinks"

    id = Column(BigInteger, primary_key=True, index=True)
    target_domain_id = Column(Integer, ForeignKey("domains.id", ondelete="CASCADE"), nullable=False, index=True)
    target_url = Column(Text, nullable=False)
    source_url = Column(Text, nullable=False)
    source_domain = Column(String(255), nullable=False, index=True)
    anchor_text = Column(Text, nullable=True)
    is_follow = Column(Boolean, default=True)
    is_active = Column(Boolean, default=True)
    provider = Column(String(50), nullable=True)
    first_seen = Column(DateTime(timezone=True), nullable=True)
    last_seen = Column(DateTime(timezone=True), nullable=True)
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())

    target_domain = relationship("Domain", back_populates="backlinks")


# ── 15. backlink_history ──────────────────────────────────────────────────────

class BacklinkHistory(Base):
    __tablename__ = "backlink_history"

    id = Column(BigInteger, primary_key=True, index=True)
    domain_id = Column(Integer, ForeignKey("domains.id", ondelete="CASCADE"), nullable=False, index=True)
    observed_date = Column(Date, nullable=False, index=True)
    total_backlinks = Column(Integer, nullable=True)
    referring_domains = Column(Integer, nullable=True)
    follow_links = Column(Integer, nullable=True)
    nofollow_links = Column(Integer, nullable=True)
    new_backlinks = Column(Integer, nullable=True)
    lost_backlinks = Column(Integer, nullable=True)
    provider = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ── 16. traffic_estimates ─────────────────────────────────────────────────────

class TrafficEstimate(Base):
    __tablename__ = "traffic_estimates"
    __table_args__ = (
        UniqueConstraint("domain_id", "keyword_id", "estimated_date", name="uq_traffic_domain_keyword_date"),
    )

    id = Column(Integer, primary_key=True, index=True)
    domain_id = Column(Integer, ForeignKey("domains.id", ondelete="CASCADE"), nullable=False, index=True)
    keyword_id = Column(Integer, ForeignKey("keywords.id", ondelete="CASCADE"), nullable=False, index=True)
    estimated_date = Column(Date, nullable=False)
    position = Column(Integer, nullable=True)
    search_volume = Column(Integer, nullable=True)
    ctr_estimate = Column(Float, nullable=True)      # the CTR model value used
    traffic_estimate = Column(Float, nullable=True)  # search_volume × ctr
    country_code = Column(String(10), nullable=False)
    device = Column(Enum(DeviceType), nullable=False)
    # Disclaimer: always label as estimate
    is_estimate = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    domain = relationship("Domain", back_populates="traffic_estimates")
    keyword = relationship("Keyword", back_populates="traffic_estimates")


# ── 17. seo_audits ────────────────────────────────────────────────────────────

class SeoAudit(Base):
    __tablename__ = "seo_audits"

    id = Column(Integer, primary_key=True, index=True)
    domain_id = Column(Integer, ForeignKey("domains.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(Enum(JobStatus), default=JobStatus.pending, nullable=False, index=True)
    score = Column(Float, nullable=True)          # 0-100 (NOT an official Google score)
    pages_audited = Column(Integer, default=0)
    critical_issues = Column(Integer, default=0)
    high_issues = Column(Integer, default=0)
    medium_issues = Column(Integer, default=0)
    low_issues = Column(Integer, default=0)
    pagespeed_desktop = Column(Float, nullable=True)
    pagespeed_mobile = Column(Float, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    domain = relationship("Domain", back_populates="seo_audits")
    issues = relationship("AuditIssue", back_populates="audit", cascade="all, delete-orphan")


# ── 18. audit_issues ──────────────────────────────────────────────────────────

class AuditIssue(Base):
    __tablename__ = "audit_issues"

    id = Column(Integer, primary_key=True, index=True)
    audit_id = Column(Integer, ForeignKey("seo_audits.id", ondelete="CASCADE"), nullable=False, index=True)
    page_url = Column(Text, nullable=True)
    issue_type = Column(String(100), nullable=False, index=True)
    severity = Column(Enum(AuditSeverity), nullable=False, index=True)
    title = Column(String(500), nullable=False)
    description = Column(Text, nullable=True)
    recommendation = Column(Text, nullable=True)
    affected_value = Column(Text, nullable=True)   # the actual problematic content
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    audit = relationship("SeoAudit", back_populates="issues")


# ── 19. scheduled_jobs ────────────────────────────────────────────────────────

class ScheduledJob(Base):
    __tablename__ = "scheduled_jobs"

    id = Column(Integer, primary_key=True, index=True)
    domain_id = Column(Integer, ForeignKey("domains.id", ondelete="CASCADE"), nullable=True)
    job_type = Column(String(50), nullable=False)   # "ranking_check", "crawl", "audit"
    frequency = Column(Enum(CheckFrequency), default=CheckFrequency.weekly, nullable=False)
    is_active = Column(Boolean, default=True)
    last_run_at = Column(DateTime(timezone=True), nullable=True)
    next_run_at = Column(DateTime(timezone=True), nullable=True)
    config = Column(JSON, nullable=True)   # job-specific params
    celery_task_id = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


# ── 20. api_usage_logs ────────────────────────────────────────────────────────

class ApiUsageLog(Base):
    __tablename__ = "api_usage_logs"

    id = Column(BigInteger, primary_key=True, index=True)
    provider = Column(String(50), nullable=False, index=True)
    endpoint = Column(String(200), nullable=False)
    method = Column(String(10), nullable=False)
    domain_id = Column(Integer, ForeignKey("domains.id", ondelete="SET NULL"), nullable=True)
    keyword_text = Column(String(500), nullable=True)
    request_count = Column(Integer, default=1)
    cost_usd = Column(Float, nullable=True)
    response_code = Column(Integer, nullable=True)
    is_cached = Column(Boolean, default=False)
    is_sandbox = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), index=True)

    __table_args__ = (
        Index("ix_api_usage_logs_provider_date", "provider", "created_at"),
    )
