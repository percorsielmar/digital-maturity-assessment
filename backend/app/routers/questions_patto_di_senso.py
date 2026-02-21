from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Organization
from app.auth import get_current_organization
from app.questions_patto_di_senso_data import PATTO_DI_SENSO_QUESTIONS, PATTO_DI_SENSO_CATEGORIES

router = APIRouter(prefix="/questions-patto-di-senso", tags=["questions-patto-di-senso"])

@router.get("/")
async def get_patto_di_senso_questions(
    organization: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db)
):
    """Get all Patto di Senso assessment questions (108 questions, 4 macro-areas)."""
    return {
        "questions": PATTO_DI_SENSO_QUESTIONS,
        "categories": PATTO_DI_SENSO_CATEGORIES,
        "total": len(PATTO_DI_SENSO_QUESTIONS)
    }

@router.get("/categories")
async def get_patto_di_senso_categories():
    """Get Patto di Senso question categories."""
    return {"categories": PATTO_DI_SENSO_CATEGORIES}
