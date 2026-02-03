from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database import get_db
from app.models import Question, Organization
from app.schemas import QuestionResponse
from app.auth import get_current_organization

router = APIRouter(prefix="/questions", tags=["questions"])

@router.get("/", response_model=List[QuestionResponse])
async def get_questions(
    organization: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Question)
        .where(
            (Question.target_type == "both") | 
            (Question.target_type == organization.type)
        )
        .order_by(Question.order)
    )
    questions = result.scalars().all()
    return [QuestionResponse.model_validate(q) for q in questions]

@router.get("/categories")
async def get_categories(
    organization: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Question.category).distinct()
    )
    categories = [row[0] for row in result.fetchall()]
    return {"categories": categories}
