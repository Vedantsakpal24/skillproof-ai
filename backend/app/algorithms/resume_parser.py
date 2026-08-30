import fitz  # PyMuPDF
import json
import re
import os

SKILLS_DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'skills_db.json')

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

def detect_skills(text: str) -> list:
    try:
        with open(SKILLS_DB_PATH, 'r') as f:
            skills_db = json.load(f)
    except FileNotFoundError:
        skills_db = ["Python", "JavaScript", "React", "Node.js", "HTML", "CSS", "SQL", "MongoDB", "MySQL", "PostgreSQL", "Java", "C++", "Docker", "Git", "GitHub", "FastAPI", "Django", "Flask", "Express.js"]

    detected = set()
    text_lower = text.lower()
    
    for skill in skills_db:
        # Use regex for word boundaries to avoid partial matches
        pattern = r'\b' + re.escape(skill.lower()) + r'\b'
        if re.search(pattern, text_lower):
            detected.add(skill)
            
    return list(detected)
