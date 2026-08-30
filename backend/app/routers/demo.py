from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.models import User, ClaimedSkill, VerifiedSkill

router = APIRouter()

@router.post("/load")
def load_demo_profile(db: Session = Depends(get_db)):
    # Clear existing data for demo
    db.query(User).delete()
    db.query(ClaimedSkill).delete()
    db.query(VerifiedSkill).delete()
    db.commit()
    
    # Create Demo User
    demo_user = User(target_role="Full Stack Developer")
    db.add(demo_user)
    db.commit()
    db.refresh(demo_user)
    
    # Add Claimed Skills
    claimed = ["Python", "JavaScript", "React", "HTML", "CSS"]
    for skill in claimed:
        db.add(ClaimedSkill(user_id=demo_user.id, skill_name=skill))
        
    # Add Verified Skills
    verified = [
        {"name": "Python", "score": 85, "level": "Advanced"},
        {"name": "JavaScript", "score": 72, "level": "Advanced"},
        {"name": "React", "score": 48, "level": "Intermediate"},
        {"name": "HTML", "score": 90, "level": "Advanced"},
        {"name": "CSS", "score": 82, "level": "Advanced"}
    ]
    for v in verified:
        db.add(VerifiedSkill(user_id=demo_user.id, skill_name=v["name"], score=v["score"], level=v["level"]))
        
    db.commit()
    
    return {"message": "Demo profile loaded successfully", "user_id": demo_user.id}
