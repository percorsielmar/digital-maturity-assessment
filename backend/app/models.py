from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, JSON, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    type = Column(String(50))  # "azienda" or "pa"
    sector = Column(String(100))
    size = Column(String(50))
    access_code = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(255))
    email = Column(String(255))
    fiscal_code = Column(String(50))  # Codice Fiscale / Partita IVA
    phone = Column(String(50))  # Numero di telefono
    admin_name = Column(String(255))  # Nome e Cognome responsabile
    created_at = Column(DateTime, default=datetime.utcnow)
    
    assessments = relationship("Assessment", back_populates="organization")

class Assessment(Base):
    __tablename__ = "assessments"
    
    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    level = Column(Integer, default=1)  # 1 = base, 2 = advanced
    status = Column(String(50), default="in_progress")  # in_progress, completed, analyzed
    responses = Column(JSON, default=dict)
    scores = Column(JSON, default=dict)
    gap_analysis = Column(JSON, default=dict)
    report = Column(Text)
    maturity_level = Column(Float)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime)
    
    organization = relationship("Organization", back_populates="assessments")

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String(100), nullable=False)
    subcategory = Column(String(100))
    text = Column(Text, nullable=False)
    hint = Column(Text)  # Tooltip/spiegazione per l'utente
    options = Column(JSON)  # List of options with scores
    weight = Column(Float, default=1.0)
    order = Column(Integer, default=0)
    target_type = Column(String(50))  # "azienda", "pa", or "both"
