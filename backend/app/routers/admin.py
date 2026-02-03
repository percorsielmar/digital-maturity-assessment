from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import os

from app.database import get_db
from app.models import Organization, Assessment
from app.schemas import OrganizationResponse, AssessmentSummary

router = APIRouter(prefix="/admin", tags=["admin"])

ADMIN_SECRET = os.getenv("ADMIN_SECRET", "admin-secret-key-change-me")

def verify_admin_key(admin_key: str):
    if admin_key != ADMIN_SECRET:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Chiave admin non valida"
        )
    return True

@router.get("/organizations")
async def get_all_organizations(
    admin_key: str,
    db: AsyncSession = Depends(get_db)
):
    verify_admin_key(admin_key)
    
    result = await db.execute(
        select(Organization).order_by(Organization.created_at.desc())
    )
    organizations = result.scalars().all()
    
    org_list = []
    for org in organizations:
        assessments_result = await db.execute(
            select(Assessment)
            .where(Assessment.organization_id == org.id)
            .order_by(Assessment.created_at.desc())
        )
        assessments = assessments_result.scalars().all()
        
        org_list.append({
            "id": org.id,
            "name": org.name,
            "type": org.type,
            "sector": org.sector,
            "size": org.size,
            "email": org.email,
            "access_code": org.access_code,
            "created_at": org.created_at.isoformat() if org.created_at else None,
            "assessments_count": len(assessments),
            "assessments": [
                {
                    "id": a.id,
                    "status": a.status,
                    "maturity_level": a.maturity_level,
                    "created_at": a.created_at.isoformat() if a.created_at else None,
                    "completed_at": a.completed_at.isoformat() if a.completed_at else None
                }
                for a in assessments
            ]
        })
    
    return {"organizations": org_list, "total": len(org_list)}

@router.get("/assessments/{assessment_id}")
async def get_assessment_detail(
    assessment_id: int,
    admin_key: str,
    db: AsyncSession = Depends(get_db)
):
    verify_admin_key(admin_key)
    
    result = await db.execute(
        select(Assessment).where(Assessment.id == assessment_id)
    )
    assessment = result.scalar_one_or_none()
    
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment non trovato"
        )
    
    org_result = await db.execute(
        select(Organization).where(Organization.id == assessment.organization_id)
    )
    organization = org_result.scalar_one_or_none()
    
    return {
        "id": assessment.id,
        "organization": {
            "id": organization.id,
            "name": organization.name,
            "type": organization.type,
            "sector": organization.sector,
            "size": organization.size
        } if organization else None,
        "status": assessment.status,
        "maturity_level": assessment.maturity_level,
        "scores": assessment.scores,
        "gap_analysis": assessment.gap_analysis,
        "report": assessment.report,
        "responses": assessment.responses,
        "created_at": assessment.created_at.isoformat() if assessment.created_at else None,
        "completed_at": assessment.completed_at.isoformat() if assessment.completed_at else None
    }

@router.get("/stats")
async def get_stats(
    admin_key: str,
    db: AsyncSession = Depends(get_db)
):
    verify_admin_key(admin_key)
    
    orgs_result = await db.execute(select(Organization))
    organizations = orgs_result.scalars().all()
    
    assessments_result = await db.execute(select(Assessment))
    assessments = assessments_result.scalars().all()
    
    completed = [a for a in assessments if a.status == "completed"]
    avg_maturity = sum(a.maturity_level or 0 for a in completed) / len(completed) if completed else 0
    
    return {
        "total_organizations": len(organizations),
        "total_assessments": len(assessments),
        "completed_assessments": len(completed),
        "in_progress_assessments": len(assessments) - len(completed),
        "average_maturity_level": round(avg_maturity, 2)
    }
