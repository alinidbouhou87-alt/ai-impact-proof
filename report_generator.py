"""PDF report generation module"""
from typing import Dict, Any, List
from datetime import datetime

def generate_report(
    output_path: str,
    project_name: str,
    impact: Dict[str, Any],
    confidence: Dict[str, Any],
    safety: Dict[str, Any],
    evidence: List[Dict[str, Any]]
) -> None:
    """
    Generate a PDF report of AI impact analysis
    
    Args:
        output_path: Path to save the PDF report
        project_name: Name of the analyzed project
        impact: Impact metrics from calculate_impact()
        confidence: Confidence metrics from calculate_confidence()
        safety: Safety report from safety_report()
        evidence: Evidence items from analyze_repository()
    """
    try:
        from reportlab.lib.pagesizes import letter, A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
        
        # Create PDF
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30,
            alignment=TA_CENTER
        )
        story.append(Paragraph("🤖 AI Impact Proof Report", title_style))
        story.append(Spacer(1, 0.3*inch))
        
        # Project Info
        story.append(Paragraph(f"<b>Project:</b> {project_name}", styles['Normal']))
        story.append(Paragraph(f"<b>Report Date:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Impact Summary
        story.append(Paragraph("<b>AI Impact Summary</b>", styles['Heading2']))
        impact_data = [
            ['Metric', 'Value'],
            ['Impact Score', f"{impact['impact_score']}/100"],
            ['Time Saved', f"{impact['time_saved']} hours"],
            ['Estimated Value', f"${impact['saved_value']}"],
            ['Net Value', f"${impact['net_value']}"],
            ['ROI', f"{impact['roi']}%"]
        ]
        impact_table = Table(impact_data)
        impact_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f77b4')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(impact_table)
        story.append(Spacer(1, 0.3*inch))
        
        # Confidence Section
        story.append(Paragraph("<b>Analysis Confidence</b>", styles['Heading2']))
        story.append(Paragraph(f"Level: {confidence['level']}", styles['Normal']))
        story.append(Paragraph(f"Score: {confidence['score']}/100", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Safety Section
        story.append(Paragraph("<b>Safety Assessment</b>", styles['Heading2']))
        story.append(Paragraph(f"Safety Score: {safety['score']}/100", styles['Normal']))
        if safety['findings']:
            story.append(Paragraph("<b>Findings:</b>", styles['Normal']))
            for finding in safety['findings']:
                story.append(Paragraph(f"• {finding}", styles['Normal']))
        else:
            story.append(Paragraph("✓ No sensitive information detected", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
        
        # Evidence Section
        if evidence:
            story.append(PageBreak())
            story.append(Paragraph("<b>AI Evidence Found</b>", styles['Heading2']))
            for item in evidence:
                story.append(Paragraph(f"<b>{item['type']}:</b> {item['title']}", styles['Normal']))
                story.append(Paragraph(f"Confidence: {item['confidence']}", styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
        
        # Build PDF
        doc.build(story)
        
    except ImportError:
        # Fallback: Create simple text report if reportlab not installed
        with open(output_path.replace('.pdf', '.txt'), 'w') as f:
            f.write("AI Impact Proof Report\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Project: {project_name}\n")
            f.write(f"Date: {datetime.now()}\n\n")
            f.write("Impact Metrics:\n")
            for key, value in impact.items():
                f.write(f"  {key}: {value}\n")
            f.write(f"\nConfidence: {confidence['level']} ({confidence['score']}/100)\n")
            f.write(f"Safety Score: {safety['score']}/100\n")
