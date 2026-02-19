from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import Organization
from app.auth import get_current_organization
from app.questions_iso56002_data import ISO56002_QUESTIONS, ISO56002_CATEGORIES

router = APIRouter(prefix="/questions-iso56002", tags=["questions-iso56002"])

@router.get("/")
async def get_iso56002_questions(
    organization: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db)
):
    """Get all ISO 56002 innovation management assessment questions."""
    return {
        "questions": ISO56002_QUESTIONS,
        "categories": ISO56002_CATEGORIES,
        "total": len(ISO56002_QUESTIONS)
    }

@router.get("/categories")
async def get_iso56002_categories():
    """Get ISO 56002 question categories."""
    return {"categories": ISO56002_CATEGORIES}
