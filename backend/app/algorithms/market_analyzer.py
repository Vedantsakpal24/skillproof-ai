import pandas as pd
import requests
import time
import os
from app.config.careers import CAREERS

_cache = {}
CACHE_DURATION = 3600  # 1 hour

def load_jobs(search_term: str = "") -> pd.DataFrame:
    global _cache
    
    # We will just fetch a massive generic pool of jobs and cache it, 
    # then strictly filter it in job_matcher to guarantee accuracy.
    # The remotive search param is too flaky to trust on its own.
    cache_key = "all_jobs"
    
    if cache_key in _cache and time.time() - _cache[cache_key]['time'] < CACHE_DURATION:
        return _cache[cache_key]['data']
        
    formatted_jobs = []
    
    try:
        # Fetch up to 1000 jobs to ensure we have enough data to filter locally
        url = "https://remotive.com/api/remote-jobs?limit=1000"
            
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        jobs_data = response.json().get("jobs", [])
        
        for job in jobs_data:
            formatted_jobs.append({
                "job_id": job.get("id"),
                "job_title": job.get("title"),
                "category": job.get("category", ""),
                "company": job.get("company_name", "Unknown"),
                "location": job.get("candidate_required_location"),
                "skills": ", ".join(job.get("tags", [])),
                "job_url": job.get("url", "#"),
                "description": job.get("description", "")
            })
    except Exception as e:
        print(f"Failed to fetch real jobs: {e}")
        
    df = pd.DataFrame(formatted_jobs) if formatted_jobs else pd.DataFrame(columns=["job_id", "job_title", "category", "company", "location", "skills", "job_url", "description"])
    _cache[cache_key] = {'data': df, 'time': time.time()}
    return df

def calculate_market_demand(target_role: str) -> dict:
    df = load_jobs()
    total_jobs = len(df)
    if total_jobs == 0: return {}
    
    # Filter the df specifically for the target_role to calculate demand
    from app.services.job_matcher import is_role_relevant
    
    relevant_jobs = []
    for idx, row in df.iterrows():
        if is_role_relevant(row['job_title'], target_role) or is_role_relevant(row['category'], target_role):
            relevant_jobs.append(row)
            
    if not relevant_jobs:
        relevant_jobs = [row for idx, row in df.iterrows()] # fallback to all
        
    skill_counts = {}
    total_relevant = len(relevant_jobs)
    
    for row in relevant_jobs:
        skills_str = row['skills']
        if pd.isna(skills_str) or not skills_str:
            continue
        skills_list = [s.strip().lower() for s in skills_str.split(',')]
        for skill in skills_list:
            skill_counts[skill] = skill_counts.get(skill, 0) + 1
            
    # Normalize keys to title case for matching
    demand = {skill.title(): (count / total_relevant) * 100 for skill, count in skill_counts.items()}
    return demand

def calculate_career_readiness(career_name: str, verified_skills: dict) -> dict:
    career_info = CAREERS.get(career_name, {"skills": []})
    required_skills = career_info["skills"]
    if not required_skills:
        return {"score": 0, "skill_weights": {}}
        
    market_demand = calculate_market_demand(career_name)
    
    skill_weights = {}
    total_weight = 0
    for skill in required_skills:
        lookup = skill.title()
        weight = market_demand.get(lookup, 10.0) 
        skill_weights[skill] = weight
        total_weight += weight
        
    if total_weight > 0:
        for skill in skill_weights:
            skill_weights[skill] = skill_weights[skill] / total_weight
    else:
        for skill in skill_weights:
            skill_weights[skill] = 1.0 / len(required_skills)
            
    readiness_score = 0
    for skill in required_skills:
        user_score = verified_skills.get(skill, 0)
        readiness_score += (user_score * skill_weights[skill])
        
    display_weights = {k: round(v * 100, 1) for k, v in skill_weights.items()}
        
    return {
        "score": round(readiness_score, 1),
        "skill_weights": display_weights
    }

def calculate_matching_opportunities(target_role: str, verified_skills: dict) -> tuple[int, int]:
    df = load_jobs()
    if df.empty:
        return 0, 0
        
    matching_count = 0
    total_role_jobs = len(df)
    
    lower_verified = {k.lower(): v for k, v in verified_skills.items()}
    
    from app.services.job_matcher import is_role_relevant
    
    for idx, row in df.iterrows():
        if not is_role_relevant(row['job_title'], target_role):
            continue
            
        skills_str = row['skills']
        if pd.isna(skills_str):
            continue
        required = [s.strip().lower() for s in skills_str.split(',')]
        if not required:
            continue
            
        met_requirements = 0
        for req in required:
            if req in lower_verified and lower_verified[req] >= 50:
                met_requirements += 1
                
        if (met_requirements / len(required)) >= 0.5:
            matching_count += 1
            
    return matching_count, total_role_jobs

def calculate_roi(target_role: str, current_skills: dict, missing_skill: str, market_demand: dict) -> dict:
    effort_map = {
        "Python": 2, "JavaScript": 2, "React": 2, "Node.js": 2, 
        "SQL": 3, "Docker": 1, "HTML": 3, "CSS": 3
    }
    effort = effort_map.get(missing_skill, 2)
    
    current_ops, _ = calculate_matching_opportunities(target_role, current_skills)
    
    simulated_skills = current_skills.copy()
    simulated_skills[missing_skill] = 80
    new_ops, _ = calculate_matching_opportunities(target_role, simulated_skills)
    
    opportunity_gain = new_ops - current_ops
    demand_weight = market_demand.get(missing_skill, 0)
    
    if effort == 0: effort = 1
    roi_score = (opportunity_gain * demand_weight) / effort
    
    if roi_score > 1000: roi_label = "HIGH"
    elif roi_score > 300: roi_label = "MEDIUM"
    else: roi_label = "LOW"
    
    return {
        "skill": missing_skill,
        "opportunity_gain": opportunity_gain,
        "roi_score": roi_score,
        "roi_label": roi_label,
        "new_opportunities": new_ops
    }
