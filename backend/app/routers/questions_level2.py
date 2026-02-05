from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from typing import List

from app.database import get_db
from app.models import Assessment, Organization
from app.auth import get_current_organization
from app.questions_level2_data import LEVEL2_QUESTIONS, LEVEL2_CATEGORIES

router = APIRouter(prefix="/questions-level2", tags=["questions-level2"])

@router.get("/")
async def get_level2_questions(
    organization: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db)
):
    """Get all level 2 questions. Requires at least one completed level 1 assessment."""
    # Check if organization has completed at least one level 1 assessment (level=1 or level=NULL)
    result = await db.execute(
        select(Assessment)
        .where(
            Assessment.organization_id == organization.id,
            or_(Assessment.level == 1, Assessment.level == None),
            Assessment.status == "completed"
        )
    )
    completed_level1 = result.scalar_one_or_none()
    
    if not completed_level1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="È necessario completare almeno un assessment di livello 1 prima di accedere al livello 2"
        )
    
    return {
        "questions": LEVEL2_QUESTIONS,
        "categories": LEVEL2_CATEGORIES,
        "total": len(LEVEL2_QUESTIONS)
    }

@router.get("/check-eligibility")
async def check_level2_eligibility(
    organization: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db)
):
    """Check if organization can access level 2 assessment."""
    # Consider level=1 or level=NULL as level 1 assessments
    result = await db.execute(
        select(Assessment)
        .where(
            Assessment.organization_id == organization.id,
            or_(Assessment.level == 1, Assessment.level == None),
            Assessment.status == "completed"
        )
    )
    completed_level1 = result.scalars().all()
    
    return {
        "eligible": len(completed_level1) > 0,
        "completed_level1_count": len(completed_level1),
        "message": "Puoi accedere all'assessment di livello 2" if len(completed_level1) > 0 else "Completa prima un assessment di livello 1"
    }
