import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # App
    APP_ENV: str = "development"
    APP_DEBUG: bool = True
    APP_SECRET_KEY: str = "change_this"
    APP_ALLOWED_ORIGINS: str = "http://localhost:3000"

    # JWT
    JWT_SECRET_KEY: str = "change_this_jwt_secret"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./rankscope.db")

    # Redis / Celery
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"

    # DataForSEO
    DATAFORSEO_LOGIN: str = ""
    DATAFORSEO_PASSWORD: str = ""
    DATAFORSEO_SANDBOX: bool = True
    DATAFORSEO_MAX_MONTHLY_SPEND_USD: float = 50.0

    # SerpApi (optional)
    SERPAPI_KEY: str = ""
    SERPAPI_ENABLED: bool = False

    # Google APIs
    GOOGLE_PAGESPEED_API_KEY: str = ""

    # AI Provider (optional)
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    AI_ENABLED: bool = False

    # Rate Limits & Cost Controls
    API_DAILY_SERP_LIMIT: int = 100
    API_MAX_CRAWL_PAGES: int = 200
    API_CRAWL_DELAY_SECONDS: float = 2.0
    API_REQUEST_TIMEOUT_SECONDS: int = 30

    @property
    def cors_origins(self) -> list:
        return [o.strip() for o in self.APP_ALLOWED_ORIGINS.split(",")]

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
