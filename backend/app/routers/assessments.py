from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, and_
from typing import List
from datetime import datetime

from app.database import get_db
from app.models import Assessment, Question, Organization
from app.schemas import AssessmentSubmit, AssessmentResponse, AssessmentSummary
from app.auth import get_current_organization
from app.crew_agents import run_crew_analysis, get_staff_profiles

router = APIRouter(prefix="/assessments", tags=["assessments"])

@router.post("/", response_model=AssessmentResponse)
async def create_assessment(
    level: int = 1,
    organization: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db)
):
    
    # For level 2, check if at least one assessment is completed
    if level == 2:
        # Cerca TUTTI gli assessment dell'organizzazione per debug
        result = await db.execute(
            select(Assessment)
            .where(Assessment.organization_id == organization.id)
        )
        all_assessments = result.scalars().all()
        
        # Log per debug
        print(f"[DEBUG] Organization {organization.id} - All assessments:")
        for a in all_assessments:
            print(f"  - ID: {a.id}, Level: {a.level}, Status: {a.status}")
        
        # Cerca assessment completati di livello 1 (o senza livello = vecchi)
        completed_level1 = [a for a in all_assessments if a.status == "completed" and a.level != 2]
        
        print(f"[DEBUG] Completed Level 1 assessments: {len(completed_level1)}")
        
        if not completed_level1:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"È necessario completare almeno un assessment di livello 1 prima di accedere al livello 2. Trovati {len(all_assessments)} assessment totali."
            )
    
    assessment = Assessment(
        organization_id=organization.id,
        level=level,
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

@router.get("/staff-profiles")
async def get_staff_profiles_endpoint():
    """Restituisce le schede profilo del personale DIH per rendicontazione UE"""
    profiles = get_staff_profiles()
    return {
        "profiles": profiles,
        "description": "Schede profilo del personale coinvolto nel programma Digital Maturity Assessment - Rome DIH"
    }

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

@router.put("/{assessment_id}/save-progress")
async def save_progress(
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
    
    if assessment.status == "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Assessment già completato"
        )
    
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
    
    assessment.responses = responses
    await db.commit()
    
    return {"success": True, "saved_answers": len(submission.answers)}

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
    
    program = getattr(organization, 'program', 'dma') or 'dma'
    
    if program == "iso56002":
        from app.questions_iso56002_data import ISO56002_QUESTIONS
        questions_for_analysis = [
            {"id": i + 1, "category": q["category"], "subcategory": q.get("subcategory"), "text": q["text"], "options": q["options"], "weight": q.get("weight", 1.0)}
            for i, q in enumerate(ISO56002_QUESTIONS)
        ]
    elif program == "governance":
        from app.questions_governance_data import GOVERNANCE_QUESTIONS
        questions_for_analysis = [
            {"id": i + 1, "category": q["category"], "subcategory": q.get("subcategory"), "text": q["text"], "options": q["options"], "weight": q.get("weight", 1.0)}
            for i, q in enumerate(GOVERNANCE_QUESTIONS)
        ]
    elif program == "patto_di_senso":
        from app.questions_patto_di_senso_data import PATTO_DI_SENSO_QUESTIONS
        questions_for_analysis = [
            {"id": i + 1, "category": q["category"], "subcategory": q.get("subcategory"), "text": q["text"], "options": q["options"], "weight": q.get("weight", 1.0)}
            for i, q in enumerate(PATTO_DI_SENSO_QUESTIONS)
        ]
    else:
        questions_for_analysis = questions_list
    
    analysis_result = await run_crew_analysis(responses, questions_for_analysis, organization_info, program=program)
    
    assessment.responses = responses
    assessment.scores = analysis_result.get("scores", {})
    assessment.gap_analysis = analysis_result.get("gap_analysis", {})
    assessment.maturity_level = analysis_result.get("overall_maturity", 0)
    assessment.report = analysis_result.get("report", "")
    assessment.audit_sheet = analysis_result.get("audit_sheet", "")
    assessment.status = "completed"
    assessment.completed_at = datetime.utcnow()
    
    await db.commit()
    await db.refresh(assessment)
    
    return AssessmentResponse.model_validate(assessment)

@router.get("/debug/check-level1")
async def debug_check_level1(
    organization: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db)
):
    """Debug endpoint to check level 1 assessment status."""
    result = await db.execute(
        select(Assessment)
        .where(Assessment.organization_id == organization.id)
    )
    all_assessments = result.scalars().all()
    
    return {
        "organization_id": organization.id,
        "total_assessments": len(all_assessments),
        "assessments": [
            {
                "id": a.id,
                "level": a.level,
                "status": a.status,
                "created_at": str(a.created_at) if a.created_at else None,
                "completed_at": str(a.completed_at) if a.completed_at else None
            }
            for a in all_assessments
        ]
    }

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
        "audit_sheet": assessment.audit_sheet,
        "scores": assessment.scores,
        "maturity_level": assessment.maturity_level,
        "gap_analysis": assessment.gap_analysis
    }

@router.get("/{assessment_id}/audit-sheet")
async def get_audit_sheet(
    assessment_id: int,
    organization: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db)
):
    """Restituisce la Scheda di Audit per rendicontazione UE"""
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
    
    if not assessment.audit_sheet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Scheda di Audit non disponibile per questo assessment"
        )
    
    return {
        "audit_sheet": assessment.audit_sheet,
        "organization_name": organization.name,
        "organization_type": organization.type,
        "maturity_level": assessment.maturity_level,
        "completed_at": assessment.completed_at
    }

@router.get("/{assessment_id}/full-documentation")
async def get_full_documentation(
    assessment_id: int,
    organization: Organization = Depends(get_current_organization),
    db: AsyncSession = Depends(get_db)
):
    """Restituisce la documentazione completa per rendicontazione UE: report, scheda audit e profili staff"""
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
    
    staff_profiles = get_staff_profiles()
    
    return {
        "organization": {
            "name": organization.name,
            "type": organization.type,
            "sector": organization.sector,
            "size": organization.size
        },
        "assessment": {
            "id": assessment.id,
            "maturity_level": assessment.maturity_level,
            "scores": assessment.scores,
            "gap_analysis": assessment.gap_analysis,
            "completed_at": assessment.completed_at
        },
        "documents": {
            "report": assessment.report,
            "audit_sheet": assessment.audit_sheet,
            "staff_profiles": staff_profiles
        }
    }
