import PyPDF2

def parse_cv(cv_path):
    #cv datei parse
    try:
        text = ""
        with open(cv_path, 'rb') as f:
            pdf = PyPDF2.PdfReader(f)
            for page in pdf.pages:
                text += page.extract_text()
        return text
    except Exception as e:
        print(f"Error: {e}")
        return ""


