import json
import os
import random
from app.services.history import get_recently_seen_questions, record_question_attempt

TECHNICAL_SKILLS = {
    'APIs', 'AWS', 'CI_CD', 'CSS', 'Docker', 'Embeddings', 'HTML', 'Hugging_Face', 
    'Image_Processing', 'JavaScript', 'Kubernetes', 'LLMs', 'MLOps', 'Machine_Learning', 
    'Node.js', 'OpenCV', 'Pandas', 'Prompt_Engineering', 'PyTorch', 'Python', 'RAG', 
    'React', 'SQL', 'Scikit_Learn', 'Selenium', 'Transformers', 'TypeScript', 'YOLO',
    'API_Testing', 'Automation'
}

def get_questions_for_skill(skill_name: str) -> list:
    filepath = os.path.join(os.path.dirname(__file__), '..', 'data', 'questions', f"{skill_name.lower()}.json")
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def generate_assessment(user_id: str, career_id: str, skill_name: str) -> list:
    if skill_name in TECHNICAL_SKILLS:
        distribution = {
            "mcq": 15,
            "coding": 5,
            "debugging": 3
        }
    else:
        distribution = {
            "mcq": 15,
            "scenario": 8
        }
    
    all_questions = get_questions_for_skill(skill_name)
    if not all_questions:
        return []
        
    previously_seen = get_recently_seen_questions(user_id, skill_name)
    
    # Filter unseen
    unseen_questions = [q for q in all_questions if q['id'] not in previously_seen]
    
    assessment = []
    
    for qtype, count in distribution.items():
        type_unseen = [q for q in unseen_questions if q.get('question_type') == qtype]
        
        # If we don't have enough unseen questions, we pull from the seen ones (cooldown fallback)
        if len(type_unseen) < count:
            type_seen = [q for q in all_questions if q.get('question_type') == qtype and q['id'] in previously_seen]
            needed = count - len(type_unseen)
            selected = type_unseen + random.sample(type_seen, min(needed, len(type_seen)))
        else:
            selected = random.sample(type_unseen, count)
            
        assessment.extend(selected)
        
    return assessment
