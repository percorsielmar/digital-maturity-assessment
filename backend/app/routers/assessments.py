from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime

from app.database import get_db
from app.models import Assessment, Question, Organization
from app.schemas import AssessmentSubmit, AssessmentResponse, AssessmentSummary
from app.auth import get_current_organization
from app.crew_agents import run_crew_analysis

router = APIRouter(prefix="/assessments", tags=["assessments"])

@router.post("/", response_model=AssessmentResponse)
async def create_assessment(
    organization: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db)
):
    assessment = Assessment(
        organization_id=organization.id,
        status="in_progress",
        responses={},
        scores={},
        gap_analysis={}
    )
    db.add(assessment)
    await db.commit()
    await db.refresh(assessment)
    return AssessmentResponse.model_validate(assessment)

@router.get("/", response_model=List[AssessmentSummary])
async def get_assessments(
    organization: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Assessment)
        .where(Assessment.organization_id == organization.id)
        .order_by(Assessment.created_at.desc())
    )
    assessments = result.scalars().all()
    return [AssessmentSummary.model_validate(a) for a in assessments]

@router.get("/{assessment_id}", response_model=AssessmentResponse)
async def get_assessment(
    assessment_id: int,
    organization: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Assessment)
        .where(
            Assessment.id == assessment_id,
            Assessment.organization_id == organization.id
        )
    )
    assessment = result.scalar_one_or_none()
    
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment non trovato"
        )
    
    return AssessmentResponse.model_validate(assessment)

@router.post("/{assessment_id}/submit", response_model=AssessmentResponse)
async def submit_assessment(
    assessment_id: int,
    submission: AssessmentSubmit,
    organization: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Assessment)
        .where(
            Assessment.id == assessment_id,
            Assessment.organization_id == organization.id
        )
    )
    assessment = result.scalar_one_or_none()
    
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment non trovato"
        )
    
    questions_result = await db.execute(select(Question))
    questions = questions_result.scalars().all()
    questions_list = [
        {
            "id": q.id,
            "category": q.category,
            "subcategory": q.subcategory,
            "text": q.text,
            "options": q.options,
            "weight": q.weight
        }
        for q in questions
    ]
    
    responses = {
        "answers": [
            {
                "question_id": a.question_id,
                "selected_option": a.selected_option,
                "notes": a.notes
            }
            for a in submission.answers
        ]
    }
    
    organization_info = {
        "name": organization.name,
        "type": organization.type,
        "sector": organization.sector,
        "size": organization.size
    }
    
    analysis_result = await run_crew_analysis(responses, questions_list, organization_info)
    
    assessment.responses = responses
    assessment.scores = analysis_result.get("scores", {})
    assessment.gap_analysis = analysis_result.get("gap_analysis", {})
    assessment.maturity_level = analysis_result.get("overall_maturity", 0)
    assessment.report = analysis_result.get("report", "")
    assessment.status = "completed"
    assessment.completed_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(assessment)
    
    return AssessmentResponse.model_validate(assessment)

@router.get("/{assessment_id}/report")
async def get_report(
    assessment_id: int,
    organization: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Assessment)
        .where(
            Assessment.id == assessment_id,
            Assessment.organization_id == organization.id
        )
    )
    assessment = result.scalar_one_or_none()
    
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Assessment non trovato"
        )
    
    if assessment.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assessment non ancora completato"
        )
    
    return {
        "report": assessment.report,
        "scores": assessment.scores,
        "maturity_level": assessment.maturity_level,
        "gap_analysis": assessment.gap_analysis
    }
