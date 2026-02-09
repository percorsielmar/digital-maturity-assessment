from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from pydantic import BaseModel
import os

from app.database import get_db
from app.models import Organization, Assessment, Question
from app.schemas import OrganizationResponse, AssessmentSummary
from app.auth import get_password_hash
from app.crew_agents import run_crew_analysis, get_staff_profiles

router = APIRouter(prefix="/admin", tags=["admin"])

ADMIN_SECRET = os.getenv("ADMIN_SECRET", "admin-secret-key-change-me")

class PasswordResetRequest(BaseModel):
    organization_id: int
    new_password: str
    admin_key: str

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
            "size": organization.size,
            "email": organization.email,
            "fiscal_code": organization.fiscal_code,
            "phone": organization.phone,
            "admin_name": organization.admin_name
        } if organization else None,
        "status": assessment.status,
        "maturity_level": assessment.maturity_level,
        "scores": assessment.scores,
        "gap_analysis": assessment.gap_analysis,
        "report": assessment.report,
        "audit_sheet": assessment.audit_sheet,
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

@router.post("/reset-password")
async def reset_password(
    request: PasswordResetRequest,
    db: AsyncSession = Depends(get_db)
):
    verify_admin_key(request.admin_key)
    
    result = await db.execute(
        select(Organization).where(Organization.id == request.organization_id)
    )
    organization = result.scalar_one_or_none()
    
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organizzazione non trovata"
        )
    
    organization.hashed_password = get_password_hash(request.new_password)
    await db.commit()
    
    return {
        "success": True,
        "message": f"Password resettata per {organization.name}",
        "organization_id": organization.id,
        "access_code": organization.access_code
    }

@router.delete("/assessments/{assessment_id}")
async def delete_assessment(
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
    
    await db.delete(assessment)
    await db.commit()
    
    return {"success": True, "message": f"Assessment #{assessment_id} eliminato"}

@router.delete("/organizations/{organization_id}")
async def delete_organization(
    organization_id: int,
    admin_key: str,
    db: AsyncSession = Depends(get_db)
):
    verify_admin_key(admin_key)
    
    result = await db.execute(
        select(Organization).where(Organization.id == organization_id)
    )
    organization = result.scalar_one_or_none()
    
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organizzazione non trovata"
        )
    
    assessments_result = await db.execute(
        select(Assessment).where(Assessment.organization_id == organization_id)
    )
    assessments = assessments_result.scalars().all()
    for assessment in assessments:
        await db.delete(assessment)
    
    await db.delete(organization)
    await db.commit()
    
    return {"success": True, "message": f"Organizzazione '{organization.name}' e tutti i suoi assessment eliminati"}

@router.post("/assessments/{assessment_id}/regenerate")
async def regenerate_assessment_report(
    assessment_id: int,
    admin_key: str,
    db: AsyncSession = Depends(get_db)
):
    """Rigenera il report DIH per un assessment esistente"""
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
    
    if assessment.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Solo gli assessment completati possono essere rigenerati"
        )
    
    org_result = await db.execute(
        select(Organization).where(Organization.id == assessment.organization_id)
    )
    organization = org_result.scalar_one_or_none()
    
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organizzazione non trovata"
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
    
    organization_info = {
        "name": organization.name,
        "type": organization.type,
        "sector": organization.sector,
        "size": organization.size
    }
    
    analysis_result = await run_crew_analysis(
        assessment.responses or {},
        questions_list,
        organization_info
    )
    
    assessment.scores = analysis_result.get("scores", {})
    assessment.gap_analysis = analysis_result.get("gap_analysis", {})
    assessment.maturity_level = analysis_result.get("overall_maturity", 0)
    assessment.report = analysis_result.get("report", "")
    assessment.audit_sheet = analysis_result.get("audit_sheet", "")
    
    await db.commit()
    
    return {
        "success": True,
        "message": f"Report rigenerato per assessment #{assessment_id}",
        "maturity_level": assessment.maturity_level,
        "has_audit_sheet": bool(assessment.audit_sheet)
    }

@router.get("/assessments/{assessment_id}/responses")
async def get_assessment_responses(
    assessment_id: int,
    admin_key: str,
    db: AsyncSession = Depends(get_db)
):
    """Restituisce le risposte dettagliate di un assessment con testo domande e opzioni scelte"""
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
    
    questions_result = await db.execute(select(Question).order_by(Question.order))
    questions = questions_result.scalars().all()
    questions_map = {q.id: q for q in questions}
    
    raw_responses = assessment.responses or {}
    answers_list = raw_responses.get("answers", [])
    if not answers_list and isinstance(raw_responses, list):
        answers_list = raw_responses
    
    detailed_responses = []
    for answer in answers_list:
        q_id = answer.get("question_id")
        selected = answer.get("selected_option")
        notes = answer.get("notes")
        
        question = questions_map.get(q_id)
        if question:
            options = question.options or []
            selected_text = ""
            selected_score = 0
            if isinstance(selected, int) and 0 <= selected < len(options):
                opt = options[selected]
                selected_text = opt.get("text", "")
                selected_score = opt.get("score", 0)
            
            detailed_responses.append({
                "question_id": q_id,
                "category": question.category,
                "subcategory": question.subcategory,
                "question_text": question.text,
                "selected_option_index": selected,
                "selected_option_text": selected_text,
                "selected_score": selected_score,
                "notes": notes,
                "all_options": [{"text": o.get("text", ""), "score": o.get("score", 0)} for o in options]
            })
    
    return {
        "assessment_id": assessment.id,
        "organization": {
            "name": organization.name if organization else "N/A",
            "type": organization.type if organization else "N/A",
        },
        "status": assessment.status,
        "maturity_level": assessment.maturity_level,
        "completed_at": assessment.completed_at.isoformat() if assessment.completed_at else None,
        "total_questions": len(detailed_responses),
        "responses": detailed_responses
    }

@router.get("/staff-profiles")
async def get_admin_staff_profiles(admin_key: str):
    """Restituisce le schede profilo del personale DIH"""
    verify_admin_key(admin_key)
    profiles = get_staff_profiles()
    return {
        "profiles": profiles,
        "description": "Schede profilo del personale DIH per rendicontazione UE"
    }
