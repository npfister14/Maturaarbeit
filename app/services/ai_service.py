import os
from ollama import Client
from app.services.cv_parser import parse_cv
from app.services.pdf_generator import generate_pdf
client = Client()

def generate_cover_letter_service(cv_path, job):

    cv = parse_cv(cv_path)

    prompt = f"""SCHREIBE NUR MIT ä,ö,ü - NIEMALS ae,oe,ue,ß!!!

Write German cover letter for {job.title} at {job.company} in {job.location}.

MANDATORY CHARACTER RULES:
YES: für, müssen, können, würde, schön, natürlich (with ä,ö,ü)
NO: fuer, muessen, koennen, wuerde, schoen (FORBIDDEN)
NO: ß is FORBIDDEN write 'ss' instead (grüssen not grüßen)

Output format:
- Plain text, 170-230 words
- Paragraphs separated by one blank line
- First line: Bewerbung als {job.title}
- Salutation: Use contact name if in job description, else "Sehr geehrte Damen und Herren,"
- 3-5 paragraphs: motivation, match requirements with CV achievements, value proposition
- Close: "Mit freundlichen Grüssen" + full name from CV

Use ONLY facts from materials below. No placeholders, no invented content.

JOB DESCRIPTION:
{job.description}

CV:
{cv}

REMEMBER: Use ä,ö,ü in ALL German words. NEVER use ae,oe,ue or ß."""



    #
    messages = [
        {
            "role": "system",
            "content": (
                "WICHTIG: Schreibe mit ä, ö, ü. NIEMALS ß - immer 'ss'. NIEMALS ae, oe, ue.\n\n"
                "You generate professional German cover letters.\n\n"
                "CHARACTER RULES (MANDATORY):\n"
                "YES: USE: ä, ö, ü, Ä, Ö, Ü\n"
                "NO: FORBIDDEN: ß, ae, oe, ue\n"
                "YES: REPLACE ß WITH: ss\n\n"
                "Example words you MUST spell correctly:\n"
                "- für (not fuer, not für)\n"
                "- müssen (not muessen, not müßen)\n"
                "- können (not koennen)\n"
                "- grüssen (not gruessen, not grüßen)\n"
                "- natürlich (not natuerlich)\n"
                "- schön (not schoen)\n\n"
                "Formatting:\n"
                "- Plain text only, paragraphs separated by one blank line\n"
                "- No Markdown, bullets, headers, or decorative characters\n"
                "- Formal \"Sie\" address\n\n"
                "Structure:\n"
                "- First line: Bewerbung als <Rolle> bei <Unternehmen>\n"
                "- Salutation (with contact name if provided, otherwise \"Sehr geehrte Damen und Herren,\")\n"
                "- 3-5 paragraphs: motivation, match requirements with achievements, value proposition\n"
                "- Close: \"Mit freundlichen Grüssen\" + full name + optional contact info\n\n"
                "Use ONLY facts from CV and job description. No placeholders, no invented content."
            )
        },
        {"role": "user", "content": prompt}
    ]

    # kei stream suscht nervig
    response = client.chat('deepseek-v3.1:671b-cloud', messages=messages, stream=False)
    full_text = response['message']['content']
    print("Generated Cover Letter Text:", full_text)
    # absolute path suscht zeigts es nd ah
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    pdf_path = os.path.join(base_dir, "uploads", "cover_letters", f"cover_letter_{job.id}.pdf")
    generate_pdf(full_text, pdf_path)

    return pdf_path
    


#def test_generate_cover_letter():
#    sample_cv = """Name: Max Mustermann
#    Ausbildung: Bachelor in Informatik
#    Berufserfahrung: 3 Jahre als Softwareentwickler bei Firma XYZ
#    Fähigkeiten: Python, Java, Webentwicklung, Datenbanken"""
#
#    sample_job = type('Job', (object,), {
#        'title': 'Softwareentwickler',
#        'company': 'Firma ABC',
#        'location': 'Berlin'
#    })()
#
#    generate_cover_letter(sample_cv, sample_job)

#test_generate_cover_letter()