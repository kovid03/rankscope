"""
Domain routes — add and retrieve domains within a project.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.dependencies import get_db, get_current_user
from app.models.models import User, Project, Domain
from app.schemas.domain import DomainCreate, DomainResponse

router = APIRouter(tags=["domains"])


def _get_project_or_404(project_id: int, user_id: int, db: Session) -> Project:
    project = (
        db.query(Project)
        .filter(Project.id == project_id, Project.user_id == user_id)
        .first()
    )
    if not project:
        raise HTTPException(status_code=404, detail="Project not found.")
    return project


@router.post("", response_model=DomainResponse, status_code=status.HTTP_201_CREATED)
def add_domain(
    payload: DomainCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    _get_project_or_404(payload.project_id, current_user.id, db)
    existing = (
        db.query(Domain)
        .filter(Domain.project_id == payload.project_id, Domain.domain == payload.domain)
        .first()
    )
    if existing:
        raise HTTPException(status_code=409, detail="Domain already added to this project.")
    domain = Domain(
        project_id=payload.project_id,
        domain=payload.domain,
        display_name=payload.display_name,
        is_primary=payload.is_primary,
    )
    db.add(domain)
    db.commit()
    db.refresh(domain)
    return domain


@router.get("", response_model=List[DomainResponse])
def list_domains(
    project_id: Optional[int] = Query(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    q = db.query(Domain).join(Project).filter(Project.user_id == current_user.id)
    if project_id is not None:
        q = q.filter(Domain.project_id == project_id)
    return q.all()


@router.get("/{domain_id}", response_model=DomainResponse)
def get_domain(
    domain_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    domain = (
        db.query(Domain)
        .join(Project)
        .filter(Domain.id == domain_id, Project.user_id == current_user.id)
        .first()
    )
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found.")
    return domain


@router.delete("/{domain_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_domain(
    domain_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    domain = (
        db.query(Domain)
        .join(Project)
        .filter(Domain.id == domain_id, Project.user_id == current_user.id)
        .first()
    )
    if not domain:
        raise HTTPException(status_code=404, detail="Domain not found.")
    db.delete(domain)
    db.commit()
