from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.models import User, ClaimedSkill
from ..schemas.schemas import ManualSkillsRequest, UserResponse

router = APIRouter()

@router.get("/detected/{user_id}")
def get_detected_skills(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"claimed_skills": []}
    return {"claimed_skills": [skill.skill_name for skill in user.claimed_skills]}

@router.post("/target-role/{user_id}")
def set_target_role(user_id: int, target_role: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.target_role = target_role
        db.commit()
        return {"message": "Role updated", "target_role": target_role}
    return {"error": "User not found"}

@router.post("/manual", response_model=UserResponse)
def submit_manual_skills(request: ManualSkillsRequest, db: Session = Depends(get_db)):
    user = User()
    db.add(user)
    db.commit()
    db.refresh(user)
    
    for skill in request.skills:
        claimed = ClaimedSkill(user_id=user.id, skill_name=skill)
        db.add(claimed)
        
    db.commit()
    db.refresh(user)
    
    return user

@router.get("/verified/{user_id}")
def get_verified_skills(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return {"error": "User not found"}
        
    return [
        {
            "skill_name": v.skill_name,
            "score": round(v.score, 1),
            "level": v.level
        }
        for v in user.verified_skills
    ]
