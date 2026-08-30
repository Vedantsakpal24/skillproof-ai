import json
import os
from datetime import datetime, timedelta

HISTORY_FILE = os.path.join(os.path.dirname(__file__), '..', 'data', 'history.json')
QUESTION_REPEAT_COOLDOWN_DAYS = 30

def _load_history():
    if not os.path.exists(HISTORY_FILE):
        return {}
    with open(HISTORY_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def _save_history(data):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def record_question_attempt(user_id, skill, question_id):
    history = _load_history()
    user_id = str(user_id)
    if user_id not in history:
        history[user_id] = {}
    if skill not in history[user_id]:
        history[user_id][skill] = {}
        
    history[user_id][skill][str(question_id)] = datetime.now().isoformat()
    _save_history(history)

def get_recently_seen_questions(user_id, skill):
    history = _load_history()
    user_id = str(user_id)
    if user_id not in history or skill not in history[user_id]:
        return []
        
    seen = []
    cutoff = datetime.now() - timedelta(days=QUESTION_REPEAT_COOLDOWN_DAYS)
    
    for q_id, timestamp_str in history[user_id][skill].items():
        attempt_time = datetime.fromisoformat(timestamp_str)
        if attempt_time > cutoff:
            seen.append(q_id)
            
    return seen
