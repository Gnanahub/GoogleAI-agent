from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(entries, output_path):
    doc = SimpleDocTemplate(output_path)
    styles = getSampleStyleSheet()
    story = [Paragraph("Root Cause Analysis Report", styles['Title']), Spacer(1, 20)]

    for e in entries:
        story.append(Paragraph(str(e), styles['Normal']))
        story.append(Spacer(1, 10))

    doc.build(story)
