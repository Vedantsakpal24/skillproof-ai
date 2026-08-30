from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models.models import User
from ..algorithms.market_analyzer import load_jobs, calculate_career_readiness
from ..services.job_matcher import process_and_filter_jobs

router = APIRouter()

@router.get('/{user_id}')
def get_personalized_dashboard(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
        
    if not user.target_role:
        raise HTTPException(status_code=400, detail='User has no target role')
        
    verified_skills_dict = {s.skill_name: {'score': s.score, 'level': s.level} for s in user.verified_skills}
    simple_scores = {s.skill_name: s.score for s in user.verified_skills}
    
    # Career readiness
    readiness = calculate_career_readiness(user.target_role, simple_scores)
    
    jobs_df = load_jobs()
    jobs_df = jobs_df.fillna("")
    jobs_list = jobs_df.to_dict('records')
    
    personalized_jobs = process_and_filter_jobs(jobs_list, user.target_role, verified_skills_dict)
    
    return {
        'career_goal': user.target_role,
        'verified_skills': [s.skill_name for s in user.verified_skills],
        'readiness_score': readiness.get('score', 0),
        'market_weights': readiness.get('skill_weights', {}),
        'jobs': personalized_jobs
    }
