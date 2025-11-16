import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

def generate_pdf(text, output_path):
    #fast ei zu eis vo reportlab docs, macht halt eifach es pdf usem text
    try:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        doc = SimpleDocTemplate(output_path, pagesize=A4,
                               rightMargin=2*cm, leftMargin=2*cm,
                               topMargin=2*cm, bottomMargin=2*cm)

        story = []
        styles = getSampleStyleSheet()

        # wenn zwei newlines, mache es zu eme paragraph
        for para in text.split('\n\n'):
            if para.strip():
                story.append(Paragraph(para, styles['Normal']))
                story.append(Spacer(1, 0.3*cm))

        doc.build(story)
        return output_path
    except Exception as e:
        print(f"Error: {e}")
        return None
