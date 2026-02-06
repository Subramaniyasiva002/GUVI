# Backend reloaded to refresh database connections
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import get_db, engine, Base
from models import Company, FinancialRecord
from processor import parse_financial_document
from ai_service import generate_financial_assessment
from dotenv import load_dotenv
import pandas as pd
import os
import traceback

load_dotenv()

# Create Tables (Simple migration for MVP)
Base.metadata.create_all(bind=engine)

# Get allowed origins from environment variable
allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to SME Financial Health Assessment Platform API"}

@app.post("/upload")
async def upload_financial_doc(file: UploadFile = File(...), db: Session = Depends(get_db)):
    import hashlib
    from models import Assessment
    
    content = await file.read()
    
    # Calculate file hash for duplicate detection
    file_hash = hashlib.md5(content).hexdigest()
    
    # Check if this exact file has been uploaded before
    existing_company = db.query(Company).filter(Company.file_hash == file_hash).first()
    
    if existing_company:
        # File already uploaded - fetch existing assessment
        latest_assessment = db.query(Assessment).filter(
            Assessment.company_id == existing_company.id
        ).order_by(Assessment.created_at.desc()).first()
        
        if latest_assessment:
            # Return existing data without reprocessing
            return {
                "message": f"This file was already uploaded. Showing existing analysis.",
                "company_id": existing_company.id,
                "duplicate": True,
                "assessment": {
                    "score": latest_assessment.overall_score,
                    "risk_level": latest_assessment.risk_level,
                    "narrative": latest_assessment.summary_narrative,
                    "recommendations": latest_assessment.recommendations
                }
            }
        else:
            # File uploaded but no assessment yet
            return {
                "message": f"File already uploaded. Please click 'Load Analysis' to generate assessment.",
                "company_id": existing_company.id,
                "duplicate": True
            }
    
    # New file - process normally
    try:
        records = parse_financial_document(content, file.filename)
        
        # Create new company with file hash
        company = Company(name="Demo SME", industry="Retail", file_hash=file_hash)
        db.add(company)
        db.commit()
        db.refresh(company)
            
        for record in records:
            db_record = FinancialRecord(
                company_id=company.id,
                category=record.get('category', 'Uncategorized'),
                amount=record.get('amount', 0.0),
                record_type=record.get('type', 'Expense'),
                date=pd.to_datetime(record.get('date')) if record.get('date') else None,
                source_document=file.filename
            )
            db.add(db_record)
        db.commit()
        
        return {"message": f"Successfully processed {len(records)} records.", "company_id": company.id, "duplicate": False}
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Processing Error: {str(e)}")

@app.post("/analyze/{company_id}")
def analyze_company_health(company_id: int, language: str = "en", db: Session = Depends(get_db)):
    """
    Analyze company financial health
    
    Args:
        company_id: ID of the company
        language: Language code for response ('en', 'hi', 'ta')
    """
    from models import Assessment
    import json
    
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Fetch records
    records = db.query(FinancialRecord).filter(FinancialRecord.company_id == company_id).all()
    # Serialize for AI
    data_for_ai = [{"category": r.category, "amount": r.amount, "type": r.record_type} for r in records]
    
    # Generate assessment in specified language
    assessment_data = generate_financial_assessment(data_for_ai, language=language)
    
    # Store assessment in database for consistency
    db_assessment = Assessment(
        company_id=company.id,
        overall_score=float(assessment_data.get('score', 0)) if str(assessment_data.get('score', 'N/A')).replace('.','').isdigit() else 0,
        risk_level=assessment_data.get('risk_level', 'Unknown'),
        summary_narrative=assessment_data.get('narrative', ''),
        recommendations=assessment_data.get('recommendations', [])
    )
    db.add(db_assessment)
    db.commit()
    db.refresh(db_assessment)
    
    return {"company": company.name, "assessment": assessment_data, "assessment_id": db_assessment.id}

@app.get("/download-report/{company_id}")
def download_report(company_id: int, db: Session = Depends(get_db)):
    """Generate and download PDF report using stored assessment"""
    from fastapi.responses import StreamingResponse
    from report_generator import generate_pdf_report
    from models import Assessment
    
    company = db.query(Company).filter(Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    
    # Fetch the latest assessment from database
    latest_assessment = db.query(Assessment).filter(
        Assessment.company_id == company_id
    ).order_by(Assessment.created_at.desc()).first()
    
    if not latest_assessment:
        raise HTTPException(status_code=404, detail="No assessment found. Please run analysis first.")
    
    # Fetch records for financial summary
    records = db.query(FinancialRecord).filter(FinancialRecord.company_id == company_id).all()
    
    # Calculate summary
    total_revenue = sum(r.amount for r in records if r.record_type == 'Revenue')
    total_expense = sum(r.amount for r in records if r.record_type == 'Expense')
    financial_summary = {
        "total_revenue": total_revenue,
        "total_expense": total_expense,
        "net_income": total_revenue - total_expense
    }
    
    # Use stored assessment data
    assessment_dict = {
        "score": latest_assessment.overall_score,
        "risk_level": latest_assessment.risk_level,
        "narrative": latest_assessment.summary_narrative,
        "recommendations": latest_assessment.recommendations
    }
    
    # Generate PDF
    pdf_buffer = generate_pdf_report(company.name, assessment_dict, financial_summary)
    
    return StreamingResponse(
        pdf_buffer,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=financial_report_{company.name.replace(' ', '_')}.pdf"}
    )
