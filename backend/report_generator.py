from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from io import BytesIO
from datetime import datetime

def generate_pdf_report(company_name: str, assessment: dict, financial_summary: dict) -> BytesIO:
    """
    Generate a PDF financial health report
    
    Args:
        company_name: Name of the company
        assessment: AI assessment dict with score, risk_level, narrative, recommendations
        financial_summary: Dict with total_revenue, total_expense, net_income
    
    Returns:
        BytesIO object containing the PDF
    """
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#1a5490'),
        spaceAfter=30,
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#2c5aa0'),
        spaceAfter=12,
    )
    
    # Title
    story.append(Paragraph("Financial Health Assessment Report", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Company Info
    story.append(Paragraph(f"<b>Company:</b> {company_name}", styles['Normal']))
    story.append(Paragraph(f"<b>Generated:</b> {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Financial Summary Table
    story.append(Paragraph("Financial Summary", heading_style))
    summary_data = [
        ['Metric', 'Amount (INR)'],
        ['Total Revenue', f"₹{financial_summary.get('total_revenue', 0):,.2f}"],
        ['Total Expenses', f"₹{financial_summary.get('total_expense', 0):,.2f}"],
        ['Net Income', f"₹{financial_summary.get('net_income', 0):,.2f}"],
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Health Score
    story.append(Paragraph("Health Score & Risk Assessment", heading_style))
    score = assessment.get('score', 'N/A')
    risk = assessment.get('risk_level', 'Unknown')
    
    score_data = [
        ['Financial Health Score', 'Risk Level'],
        [f"{score}/100", risk],
    ]
    
    score_table = Table(score_data, colWidths=[2.5*inch, 2.5*inch])
    score_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2c5aa0')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, -1), 18),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.lightgreen if risk == 'Low' else colors.lightyellow if risk == 'Medium' else colors.lightcoral),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Assessment Narrative
    story.append(Paragraph("Detailed Assessment", heading_style))
    narrative = assessment.get('narrative', 'No assessment available')
    story.append(Paragraph(narrative, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Recommendations
    story.append(Paragraph("Recommendations", heading_style))
    recommendations = assessment.get('recommendations', [])
    if recommendations:
        for i, rec in enumerate(recommendations, 1):
            rec_text = rec if isinstance(rec, str) else rec.get('title', str(rec))
            story.append(Paragraph(f"{i}. {rec_text}", styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
    else:
        story.append(Paragraph("No specific recommendations available.", styles['Normal']))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer
