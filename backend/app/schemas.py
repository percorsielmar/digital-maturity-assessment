from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

class OrganizationCreate(BaseModel):
    name: str
    type: str
    sector: Optional[str] = None
    size: Optional[str] = None
    email: Optional[str] = None
    fiscal_code: Optional[str] = None
    phone: Optional[str] = None
    admin_name: Optional[str] = None
    password: str

class OrganizationResponse(BaseModel):
    id: int
    name: str
    type: str
    sector: Optional[str]
    size: Optional[str]
    email: Optional[str]
    fiscal_code: Optional[str]
    phone: Optional[str]
    admin_name: Optional[str]
    access_code: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str
    organization: OrganizationResponse

class LoginRequest(BaseModel):
    access_code: str
    password: str

class QuestionOption(BaseModel):
    text: str
    score: float

class QuestionResponse(BaseModel):
    id: int
    category: str
    subcategory: Optional[str]
    text: str
    hint: Optional[str]
    options: List[QuestionOption]
    weight: float
    order: int
    
    class Config:
        from_attributes = True

class AnswerSubmit(BaseModel):
    question_id: int
    selected_option: int
    notes: Optional[str] = None

class AssessmentSubmit(BaseModel):
    answers: List[AnswerSubmit]

class AssessmentResponse(BaseModel):
    id: int
    organization_id: int
    level: int = 1
    status: str
    scores: Optional[Dict[str, Any]]
    maturity_level: Optional[float]
    gap_analysis: Optional[Dict[str, Any]]
    report: Optional[str]
    responses: Optional[Dict[str, Any]]
    created_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class AssessmentSummary(BaseModel):
    id: int
    level: int = 1
    status: str
    maturity_level: Optional[float]
    created_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True
