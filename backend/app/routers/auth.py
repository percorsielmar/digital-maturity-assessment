from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import timedelta
from pydantic import BaseModel
from google.oauth2 import id_token
from google.auth.transport import requests
import os

from app.database import get_db
from app.models import Organization
from app.schemas import OrganizationCreate, OrganizationResponse, Token, LoginRequest
from app.auth import (
    get_password_hash, 
    verify_password, 
    create_access_token, 
    generate_access_code,
    get_current_organization
)
from app.config import get_settings

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID", "776005980883-iodb4evtm9imedvilsihmfajpauj8mrn.apps.googleusercontent.com")

router = APIRouter(prefix="/auth", tags=["authentication"])
settings = get_settings()

@router.post("/register", response_model=Token)
async def register_organization(
    org_data: OrganizationCreate,
    db: AsyncSession = Depends(get_db)
):
    access_code = generate_access_code()
    
    existing = await db.execute(
        select(Organization).where(Organization.access_code == access_code)
    )
    while existing.scalar_one_or_none():
        access_code = generate_access_code()
        existing = await db.execute(
            select(Organization).where(Organization.access_code == access_code)
        )
    
    organization = Organization(
        name=org_data.name,
        type=org_data.type,
        sector=org_data.sector,
        size=org_data.size,
        email=org_data.email,
        access_code=access_code,
        hashed_password=get_password_hash(org_data.password)
    )
    
    db.add(organization)
    await db.commit()
    await db.refresh(organization)
    
    access_token = create_access_token(
        data={"sub": str(organization.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        organization=OrganizationResponse.model_validate(organization)
    )

@router.post("/login", response_model=Token)
async def login(
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Organization).where(Organization.access_code == login_data.access_code.upper())
    )
    organization = result.scalar_one_or_none()
    
    if not organization or not verify_password(login_data.password, organization.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Codice di accesso o password non validi",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token = create_access_token(
        data={"sub": str(organization.id)},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    return Token(
        access_token=access_token,
        token_type="bearer",
        organization=OrganizationResponse.model_validate(organization)
    )

@router.get("/me", response_model=OrganizationResponse)
async def get_current_org(
    organization: Organization = Depends(get_current_organization)
):
    return OrganizationResponse.model_validate(organization)

class GoogleLoginRequest(BaseModel):
    credential: str
    org_name: str = None
    org_type: str = "azienda"

@router.post("/google", response_model=Token)
async def google_login(
    google_data: GoogleLoginRequest,
    db: AsyncSession = Depends(get_db)
):
    try:
        idinfo = id_token.verify_oauth2_token(
            google_data.credential, 
            requests.Request(), 
            GOOGLE_CLIENT_ID
        )
        
        email = idinfo.get('email')
        name = idinfo.get('name', google_data.org_name or email.split('@')[0])
        
        if not email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email non trovata nel token Google"
            )
        
        result = await db.execute(
            select(Organization).where(Organization.email == email)
        )
        organization = result.scalar_one_or_none()
        
        if not organization:
            access_code = generate_access_code()
            existing = await db.execute(
                select(Organization).where(Organization.access_code == access_code)
            )
            while existing.scalar_one_or_none():
                access_code = generate_access_code()
                existing = await db.execute(
                    select(Organization).where(Organization.access_code == access_code)
                )
            
            organization = Organization(
                name=name,
                type=google_data.org_type,
                email=email,
                access_code=access_code,
                hashed_password=get_password_hash(access_code)
            )
            db.add(organization)
            await db.commit()
            await db.refresh(organization)
        
        access_token = create_access_token(
            data={"sub": str(organization.id)},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            organization=OrganizationResponse.model_validate(organization)
        )
        
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token Google non valido: {str(e)}"
        )
