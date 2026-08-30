from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
import uuid
import math
from app.database import get_db
from app.models.models import User, VerifiedSkill
from app.algorithms.adaptive_quiz import generate_assessment
from app.algorithms.market_analyzer import calculate_career_readiness
from app.services.history import record_question_attempt

router = APIRouter()

# Simple in-memory session store for MVP
sessions = {}

class QuizAnswer(BaseModel):
    question_id: str
    selected_option: int

@router.post('/start/{user_id}/{skill_name}')
def start_verification(user_id: str, skill_name: str, target_role: str = "Frontend Developer", db: Session = Depends(get_db)):
    session_id = f"{user_id}_{skill_name}_{uuid.uuid4().hex[:6]}"
    
    # Generate the 23-question assessment array
    assessment = generate_assessment(user_id, target_role, skill_name)
    if not assessment:
        raise HTTPException(status_code=404, detail="No questions available for this skill")
        
    sessions[session_id] = {
        'user_id': user_id,
        'skill_name': skill_name,
        'target_role': target_role,
        'questions': assessment,
        'current_index': 0,
        'score': 0
    }
    
    first_q = assessment[0]
    # record attempt
    record_question_attempt(user_id, skill_name, first_q['id'])
    
    return {
        'session_id': session_id,
        'question': first_q,
        'total_questions': len(assessment),
        'current_index': 0
    }

@router.post('/quiz/{session_id}')
def submit_quiz_answer(session_id: str, payload: QuizAnswer, db: Session = Depends(get_db)):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
        
    sess = sessions[session_id]
    questions = sess['questions']
    idx = sess['current_index']
    
    if idx >= len(questions):
        raise HTTPException(status_code=400, detail="Assessment already completed")
        
    current_q = questions[idx]
    
    # Simple scoring: Easy=10, Medium=20, Hard=30
    diff = current_q.get('difficulty', 'Easy')
    pts = 10 if diff == 'Easy' else 20 if diff == 'Medium' else 30
    
    is_correct = False
    if current_q.get('question_type') in ['mcq', 'scenario', 'case_study']:
        if payload.selected_option == current_q.get('correct_option'):
            sess['score'] += pts
            is_correct = True
    elif current_q.get('question_type') in ['coding', 'debugging']:
        # Simulate successful execution for sandbox tasks
        sess['score'] += pts
        is_correct = True
            
    # Move to next question
    sess['current_index'] += 1
    next_idx = sess['current_index']
    
    result = {
        "correct": is_correct,
        "explanation": current_q.get('explanation', ''),
        "correct_answer_text": current_q.get('options', [])[current_q.get('correct_option', 0)] if 'options' in current_q and current_q.get('correct_option') is not None else ""
    }
    
    if next_idx < len(questions):
        next_q = questions[next_idx]
        record_question_attempt(sess['user_id'], sess['skill_name'], next_q['id'])
        return {
            'phase': 'quiz',
            'result': result,
            'next_question': next_q,
            'progress': f"{next_idx + 1}/{len(questions)}"
        }
    else:
        # Assessment complete
        # Calculate true max score dynamically based on the exact assigned questions
        max_score = sum([10 if q.get('difficulty') == 'Easy' else 20 if q.get('difficulty') == 'Medium' else 30 for q in questions])
        final_percentage = min(100, (sess['score'] / max_score) * 100) if max_score > 0 else 0
        level = "Senior" if final_percentage > 80 else "Mid-Level" if final_percentage > 50 else "Junior"
        
        # Save to DB
        user_id_int = int(sess['user_id'])
        user = db.query(User).filter(User.id == user_id_int).first()
        if user:
            # Check if skill already exists, update if it does
            existing_skill = db.query(VerifiedSkill).filter(
                VerifiedSkill.user_id == user_id_int,
                VerifiedSkill.skill_name == sess['skill_name']
            ).first()
            
            if existing_skill:
                existing_skill.score = final_percentage
                existing_skill.level = level
            else:
                new_skill = VerifiedSkill(
                    user_id=user_id_int,
                    skill_name=sess['skill_name'],
                    score=final_percentage,
                    level=level
                )
                db.add(new_skill)
            db.commit()
        
        return {
            'phase': 'result',
            'result': result,
            'score': final_percentage,
            'level': level
        }
