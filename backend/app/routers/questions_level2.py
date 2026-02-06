from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
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
    # Check if organization has completed at least one level 1 assessment
    result = await db.execute(
        select(Assessment)
        .where(
            Assessment.organization_id == organization.id,
            Assessment.status == "completed"
        )
    )
    all_completed = result.scalars().all()
    
    # Filtra: accetta level=1, level=None, o qualsiasi level diverso da 2
    completed_level1 = [a for a in all_completed if a.level != 2]
    
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
    # Cerca tutti gli assessment completati
    result = await db.execute(
        select(Assessment)
        .where(
            Assessment.organization_id == organization.id,
            Assessment.status == "completed"
        )
    )
    all_completed = result.scalars().all()
    
    # Filtra: accetta level != 2 (include level=1, level=None, ecc.)
    completed_level1 = [a for a in all_completed if a.level != 2]
    
    return {
        "eligible": len(completed_level1) > 0,
        "completed_level1_count": len(completed_level1),
        "message": "Puoi accedere all'assessment di livello 2" if len(completed_level1) > 0 else "Completa prima un assessment di livello 1"
    }
