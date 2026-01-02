import pdfplumber
from docx import Document

def parse_cv(cv_path):
    try:
        if cv_path.endswith('.docx'):
            doc = Document(cv_path)
            return '\n'.join([p.text for p in doc.paragraphs])

        text = ""
        with pdfplumber.open(cv_path) as pdf:
            for page in pdf.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        return text.strip()
    except Exception as e:
        print(f"Error: {e}")
        return ""


