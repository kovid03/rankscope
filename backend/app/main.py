"""
RankScope FastAPI Application Entrypoint
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import Base, engine
from app.api.routes import auth, projects, domains, health
import app.models.models  # ensure models are registered

# Create database tables (SQLite in dev, Postgres in prod via Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="RankScope API",
    description="AI-Powered SEO Intelligence, Google Ranking & Competitor Analysis Platform",
    version="0.1.0",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.APP_DEBUG else settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(health.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1/auth")
app.include_router(projects.router, prefix="/api/v1/projects")
app.include_router(domains.router, prefix="/api/v1/domains")


@app.get("/")
def root():
    return {
        "app": "RankScope API",
        "version": "0.1.0",
        "status": "online",
        "docs_url": "/docs",
    }
