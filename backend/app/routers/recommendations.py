from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.models import User
from ..schemas.schemas import SimulationRequest
from ..algorithms.market_analyzer import calculate_roi, calculate_market_demand

router = APIRouter()

@router.post("/simulate/{user_id}")
def simulate_opportunity(user_id: int, request: SimulationRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.target_role:
        return {"error": "User or target role not found"}
        
    verified_skills_dict = {s.skill_name: s.score for s in user.verified_skills}
    market_demand = calculate_market_demand(user.target_role)
    
    roi_result = calculate_roi(user.target_role, verified_skills_dict, request.skill_name, market_demand)
    return roi_result

@router.get("/best-next-skill/{user_id}")
def get_best_next_skill(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user or not user.target_role:
        return {"error": "User or target role not found"}
        
    verified_skills_dict = {s.skill_name: s.score for s in user.verified_skills}
    market_demand = calculate_market_demand(user.target_role)
    
    # Identify missing skills
    all_skills_in_demand = list(market_demand.keys())
    missing_skills = [s for s in all_skills_in_demand if s not in verified_skills_dict or verified_skills_dict[s] < 40]
    
    best_skill = None
    best_roi = -1
    best_result = None
    
    for skill in missing_skills:
        roi = calculate_roi(user.target_role, verified_skills_dict, skill, market_demand)
        if roi["roi_score"] > best_roi:
            best_roi = roi["roi_score"]
            best_skill = skill
            best_result = roi
            
    if best_result:
        return {
            "recommendation": best_skill,
            "reason": [
                f"High market demand ({market_demand.get(best_skill, 0):.1f}%)",
                "Currently missing or weak in your profile",
                f"Unlocks {best_result['opportunity_gain']} new opportunities",
                f"Provides {best_result['roi_label']} ROI"
            ],
            "details": best_result
        }
        
    return {"recommendation": "None", "reason": ["You are already a master of all required skills!"]}
