"""
Health check endpoint.
"""
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    return {"status": "ok", "version": "0.1.0", "service": "RankScope API"}
