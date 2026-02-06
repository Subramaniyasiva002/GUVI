from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base

class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    industry = Column(String)
    gst_number = Column(String, unique=True, nullable=True)
    file_hash = Column(String, nullable=True, index=True)  # Hash of uploaded file for duplicate detection
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    financial_records = relationship("FinancialRecord", back_populates="company")
    assessments = relationship("Assessment", back_populates="company")

class FinancialRecord(Base):
    __tablename__ = "financial_records"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    record_type = Column(String) # Revenue, Expense, Asset, Liability
    category = Column(String) # Specific category e.g., "Sales", "Rent"
    amount = Column(Float)
    currency = Column(String, default="INR")
    date = Column(DateTime)
    source_document = Column(String, nullable=True) # Filename or ID
    
    company = relationship("Company", back_populates="financial_records")

class Assessment(Base):
    __tablename__ = "assessments"

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey("companies.id"))
    overall_score = Column(Float) # 0-100 Financial Health Score
    risk_level = Column(String) # Low, Medium, High
    summary_narrative = Column(Text) # LLM generated summary
    recommendations = Column(JSON) # Structured list of recommendations
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    company = relationship("Company", back_populates="assessments")
