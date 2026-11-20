# RankScope — Database Schema Documentation

RankScope uses a 3NF normalized schema designed for high-concurrency ingestion and historical ranking queries.

---

## 1. Schema Overview (20 Core Models)

| Table | Entity | Purpose |
|---|---|---|
| `users` | User | User accounts, credentials, and verification state |
| `projects` | Project | Organizational workspace grouping target domains |
| `domains` | Domain | Target websites and competitor domains |
| `competitors` | Competitor | M:N association mapping competitors to target domains |
| `crawled_pages` | CrawledPage | Stored crawl metadata: titles, H1-H3, status, links, canonicals |
| `crawl_jobs` | CrawlJob | Crawler task tracking, progress, and error logging |
| `keywords` | Keyword | Canonical keyword dictionary with locale & country |
| `keyword_metrics` | KeywordMetrics | Search volume, CPC, difficulty, trend data |
| `keyword_sources` | KeywordSource | Classification: discovered, candidate, verified, competitor |
| `serp_snapshots` | SerpSnapshot | SERP request metadata: timestamp, provider, depth, cost |
| `serp_results` | SerpResult | Top 100 search result entries per snapshot |
| `ranking_positions` | RankingPosition | Current verified ranking state of a domain for a keyword |
| `ranking_history` | RankingHistory | Append-only timeseries of ranking changes over time |
| `backlinks` | Backlink | Extracted or provider-sourced backlinks and anchors |
| `backlink_history` | BacklinkHistory | Aggregated daily backlink counters and referring domains |
| `traffic_estimates` | TrafficEstimate | Monthly estimated organic traffic calculations |
| `seo_audits` | SeoAudit | Technical site audit summary, scores, and PageSpeed metrics |
| `audit_issues` | AuditIssue | Granular SEO defects (broken links, missing tags, canonicals) |
| `scheduled_jobs` | ScheduledJob | Automation cron definitions for recurring rank checks |
| `api_usage_logs` | ApiUsageLog | Audit trail of third-party API consumption and spend |

---

## 2. Key Relationships & Integrity Constraints
- **Multi-Tenant Scoping:** All domains and projects cascade delete when parent records are removed (`ON DELETE CASCADE`).
- **History Immutability:** `ranking_history` and `api_usage_logs` are write-only tables to preserve audit records.
- **Deduplication:** Unique constraints on `(keyword_text, country_code, language_code)` prevent redundant API queries.
