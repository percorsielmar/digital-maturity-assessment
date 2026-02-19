from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Organization
from app.auth import get_current_organization
from app.questions_governance_data import GOVERNANCE_QUESTIONS, GOVERNANCE_CATEGORIES

router = APIRouter(prefix="/questions-governance", tags=["questions-governance"])

@router.get("/")
async def get_governance_questions(
    organization: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db)
):
    """Get all Governance Trasparente assessment questions."""
    return {
        "questions": GOVERNANCE_QUESTIONS,
        "categories": GOVERNANCE_CATEGORIES,
        "total": len(GOVERNANCE_QUESTIONS)
    }

@router.get("/categories")
async def get_governance_categories():
    """Get Governance Trasparente question categories."""
    return {"categories": GOVERNANCE_CATEGORIES}
