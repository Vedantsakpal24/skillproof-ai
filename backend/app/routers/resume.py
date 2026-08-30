from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.models import User, ClaimedSkill
from ..schemas.schemas import UserResponse
from ..algorithms.resume_parser import extract_text_from_pdf, detect_skills

router = APIRouter()

@router.post("/upload", response_model=UserResponse)
async def upload_resume(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    contents = await file.read()
    try:
        text = extract_text_from_pdf(contents)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Could not parse PDF: {str(e)}")
        
    detected_skills = detect_skills(text)
    
    # For MVP, we will create a new user per upload or just keep a single session user.
    # Let's create a new user.
    user = User()
    db.add(user)
    db.commit()
    db.refresh(user)
    
    for skill in detected_skills:
        claimed_skill = ClaimedSkill(user_id=user.id, skill_name=skill)
        db.add(claimed_skill)
        
    db.commit()
    db.refresh(user)
    
    return user
