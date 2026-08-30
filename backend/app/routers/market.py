from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.models import User
from ..algorithms.market_analyzer import calculate_market_demand, calculate_matching_opportunities

router = APIRouter()

@router.get("/demand/{user_id}")
def get_market_demand(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.target_role:
        return {"error": "User or target role not found"}
        
    demand = calculate_market_demand(user.target_role)
    return {"demand": demand}

@router.get("/match/{user_id}")
def get_market_match(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.target_role:
        return {"error": "User or target role not found"}
        
    verified_skills_dict = {s.skill_name: s.score for s in user.verified_skills}
    opportunities, total_jobs = calculate_matching_opportunities(user.target_role, verified_skills_dict)
    
    match_percentage = (opportunities / total_jobs) * 100 if total_jobs > 0 else 0
    
    return {
        "matching_opportunities": opportunities,
        "total_jobs": total_jobs,
        "match_percentage": match_percentage
    }
