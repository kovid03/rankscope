# RankScope — Architecture & System Design

RankScope is an enterprise-grade, independent SEO intelligence platform inspired by SEMrush, Ahrefs, and Moz.

---

## 1. High-Level System Architecture

```mermaid
graph TD
    User([User / Browser])
    
    subgraph Frontend ["Frontend Tier (Next.js 14 / TypeScript / Tailwind)"]
        UI[App Router & Dashboard]
        Charts[Recharts Visualization]
        State[React Context / Auth Store]
    end

    subgraph Backend ["Backend Tier (FastAPI / Python 3.9+)"]
        API[FastAPI Gateway / REST Endpoints]
        Auth[JWT & Security Middleware]
        SSRF[SSRF Protection Layer]
        SERP_Eng[SERP Ranking Engine]
        Crawl_Eng[Competitor Website Crawler]
        Audit_Eng[Technical SEO Audit Engine]
        Traffic_Eng[Organic Traffic Estimation Engine]
    end

    subgraph Workers ["Async Task Workers (Celery & Redis)"]
        Broker[(Redis Queue & Cache)]
        CeleryWorkers[Celery Worker Cluster]
        CeleryBeat[Celery Beat Scheduler]
    end

    subgraph Database ["Data Storage Tier"]
        Postgres[(PostgreSQL / SQLite in dev)]
        Timeseries[Historical SERP & Ranking Snapshots]
    end

    subgraph Providers ["External SEO Providers & Public Web"]
        DataForSEO[DataForSEO SERP API]
        PageSpeed[Google PageSpeed Insights API]
        PublicWeb[Target Domains / Public Websites]
    end

    User -->|HTTPS| UI
    UI -->|REST / Bearer Auth| API
    API --> Auth
    API --> Postgres
    API --> Broker
    CeleryWorkers --> Broker
    CeleryBeat --> Broker
    CeleryWorkers --> Postgres
    CeleryWorkers --> SSRF
    SSRF --> PublicWeb
    CeleryWorkers --> DataForSEO
    CeleryWorkers --> PageSpeed
```

---

## 2. Core Subsystems

### A. Modular SERP Engine (`app.services.serp`)
- **Abstract Provider Interface:** `BaseSerpProvider` decoupling backend business logic from data vendors.
- **DataForSEO Integration:** Direct JSON REST communication targeting Google Organic SERP API with support for device, location, and language parameters.
- **Mock Provider:** Deterministic mock provider for CI/CD and cost-free local testing.

### B. High-Performance Website Crawler (`app.crawlers`)
- Built using **HTTPX** and **BeautifulSoup4** (with Playwright headless browser fallback for JS-heavy client apps).
- **Hardened SSRF Guard:** Strict URL validation preventing access to RFC 1918, loopback (127.0.0.1), link-local, AWS metadata endpoints (169.254.169.254), and internal network ranges.
- **Politeness & Compliance:** Configurable crawl delay, depth limits, page caps, and robots.txt checking.

### C. Ranking & History Pipeline (`app.models.models`)
- Normalized schema maintaining an append-only `ranking_history` table for tracking keyword position movements, new rankings, and lost rankings.

### D. Traffic Estimation Model
- Formula: $\text{Estimated Organic Traffic} = \text{Search Volume} \times \text{Position CTR Curve}$
- Clear labeling on all outputs indicating estimations vs verified rank observations.
