# RankScope 🎯

> **AI-Powered SEO Intelligence, Google Ranking & Competitor Analysis Platform**

RankScope is an independent SEO intelligence platform inspired by SEMrush, Ahrefs, and Moz. It allows users to analyze ANY publicly accessible website domain — without requiring access to that website's private Google Search Console or analytics accounts.

---

## 🏗️ Build Status

| Phase | Description | Status |
|-------|-------------|--------|
| **Phase 1** | Repository foundation, project structure, Docker, database schema | ✅ Complete |
| **Phase 2** | FastAPI backend, PostgreSQL, Alembic migrations, auth | 🔨 In Progress |
| **Phase 3** | DataForSEO SERP integration, ranking engine | 🔜 Next |
| **Phase 4** | Competitor website crawler (Scrapy + HTTPX) | 🔜 Planned |
| **Phase 5** | Keyword discovery engine | 🔜 Planned |
| **Phase 6** | Ranking history & scheduling | 🔜 Planned |
| **Phase 7** | Competitor comparison & keyword gap | 🔜 Planned |
| **Phase 8** | Organic traffic estimation | 🔜 Planned |
| **Phase 9** | Technical SEO audit + PageSpeed API | 🔜 Planned |
| **Phase 10** | Backlink analysis | 🔜 Planned |
| **Phase 11** | AI recommendation engine | 🔜 Planned |
| **Phase 12** | Next.js dashboard (13 pages) | 🔜 Planned |
| **Phase 13** | Integration testing & security review | 🔜 Planned |
| **Phase 14** | Documentation & release | 🔜 Planned |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Python 3.9+ · FastAPI · Pydantic |
| **Database** | PostgreSQL · SQLAlchemy 2.0 · Alembic |
| **Background Jobs** | Celery · Redis |
| **Web Crawling** | Scrapy · BeautifulSoup · HTTPX · Playwright |
| **Frontend** | Next.js 14 · React · TypeScript · Tailwind CSS · Recharts |
| **SEO Data** | DataForSEO API · Google PageSpeed Insights API |
| **Testing** | Pytest · React Testing Library · Playwright E2E |
| **Infrastructure** | Docker · Docker Compose |

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose **OR**
- Python 3.9+, Node.js 18+, PostgreSQL, Redis

### With Docker (Recommended)

```bash
git clone https://github.com/sarthakJain1008/rankscope.git
cd rankscope
cp .env.example .env
# Edit .env with your credentials
docker-compose up -d
```

API: http://localhost:8000/docs
Frontend: http://localhost:3000

### Local Development

See [DEVELOPMENT_GUIDE.md](docs/DEVELOPMENT_GUIDE.md)

---

## 📐 Architecture

See [ARCHITECTURE.md](docs/ARCHITECTURE.md)

---

## 🗄️ Database Schema

See [DATABASE_SCHEMA.md](docs/DATABASE_SCHEMA.md) — 20 normalized PostgreSQL tables.

---

## 🔐 Security

- Never exposes private GSC or analytics data
- All traffic numbers are clearly labelled as estimates
- SSRF protection on all crawler endpoints
- JWT authentication
- API key stored only in backend environment variables

See [SECURITY.md](docs/SECURITY.md)

---

## ⚠️ Important Disclaimers

- **Traffic numbers are estimates** based on keyword search volume × CTR models. They are not actual visitor statistics.
- **Ranking data is observed** from public search results at the time of the check. It does not represent real-time rankings.
- **Backlink data** comes from licensed third-party providers with their own coverage limitations.
- **RankScope never accesses** any website's private Google Search Console, Analytics, or backend systems.

---

## 👥 Team

| Name | Roll No | Role |
|------|---------|------|
| Sarthak Jain | E23CSEU1494 | Team Lead |
| Kovid Chhabra | E23CSEU1491 | Developer |
| Kumar Shubham | E23CSEU1510 | Developer |

**Institution:** Bennett University | **Course:** CSET400C Capstone Project

---

## 📄 License

Academic project — not for commercial use.
