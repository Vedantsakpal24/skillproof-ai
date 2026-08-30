ROLE_KEYWORDS = {
    'Frontend Developer': ['frontend', 'front end', 'react', 'vue', 'angular', 'ui developer', 'web developer'],
    'Backend Developer': ['backend', 'back end', 'python', 'java ', 'ruby', 'node', 'api developer', 'backend engineer'],
    'Full Stack Developer': ['full stack', 'fullstack', 'full-stack', 'software engineer', 'web developer'],
    'Data Analyst': ['data analyst', 'data analysis', 'analytics', 'business intelligence', 'bi analyst'],
    'QA Tester': ['qa', 'quality assurance', 'tester', 'test engineer', 'automation engineer'],
    'DevOps Engineer': ['devops', 'sre', 'site reliability', 'platform engineer', 'infrastructure'],
    'UI/UX Designer': ['ui/ux', 'ui designer', 'ux designer', 'product designer', 'user experience'],
    'Digital Marketing Specialist': ['digital marketing', 'marketing specialist', 'seo', 'growth hacker', 'marketing manager'],
    'Machine Learning Engineer': ['machine learning', 'ml engineer', 'deep learning', 'ai engineer'],
    'Data Scientist': ['data scientist', 'data science', 'statistician'],
    'AI Engineer': ['ai engineer', 'artificial intelligence', 'llm', 'generative ai', 'prompt engineer'],
    'NLP Engineer': ['nlp', 'natural language', 'computational linguist'],
    'Computer Vision Engineer': ['computer vision', 'cv engineer', 'image processing', 'perception engineer'],
    'Cybersecurity Analyst': ['cybersecurity', 'security analyst', 'infosec', 'penetration tester', 'security engineer'],
    'Sales Representative / Business Development': ['sales', 'business development', 'account executive', 'bdr', 'sdr'],
    'Product Manager': ['product manager', 'product owner', 'technical pm']
}

def is_role_relevant(job_title: str, selected_role: str) -> bool:
    if not job_title or not selected_role: return False
    title_lower = job_title.lower()
    
    # 1. Direct string match
    if selected_role.lower() in title_lower:
        return True
        
    # 2. Keyword match
    keywords = ROLE_KEYWORDS.get(selected_role, [selected_role.lower()])
    for kw in keywords:
        if kw in title_lower:
            return True
            
    return False

def calculate_match_score(job_skills: list, verified_skills: dict) -> dict:
    if not job_skills: return {'match_score': 0, 'matched': [], 'partial': [], 'missing': []}
    matched, partial, missing = [], [], []
    total_score = 0.0
    for req in job_skills:
        req_clean = req.strip()
        req_lower = req_clean.lower()
        user_skill = next(({'name': k, 'data': v} for k, v in verified_skills.items() if k.lower() == req_lower), None)
        if user_skill:
            score = user_skill['data']['score']
            if score >= 80: matched.append(user_skill['name']); total_score += 1.0
            elif score >= 60: matched.append(user_skill['name']); total_score += 0.8
            elif score >= 40: partial.append(user_skill['name']); total_score += 0.5
            else: missing.append(req_clean)
        else: missing.append(req_clean)
    match_percentage = (total_score / len(job_skills)) * 100 if job_skills else 0
    return {'match_score': round(match_percentage), 'matched': matched, 'partial': partial, 'missing': missing}

def process_and_filter_jobs(jobs: list, selected_role: str, verified_skills: dict):
    valid_jobs = []
    for job in jobs:
        # STRICT FILTERING: The job MUST be relevant to the chosen career path!
        if not is_role_relevant(job['job_title'], selected_role) and not is_role_relevant(job.get('category', ''), selected_role):
            continue
            
        skills_list = [s.strip() for s in job['skills'].split(',')] if job.get('skills') else []
        match_result = calculate_match_score(skills_list, verified_skills)
        
        valid_jobs.append({
            'title': job['job_title'], 'company': job.get('company', 'Unknown'),
            'location': job['location'], 'match_score': match_result['match_score'],
            'matched_skills': match_result['matched'], 'partial_skills': match_result['partial'],
            'missing_skills': match_result['missing'], 'job_url': job.get('job_url', '#')
        })
        
    valid_jobs.sort(key=lambda x: x['match_score'], reverse=True)
    
    # Return top 25 best matches to keep the UI clean
    return valid_jobs[:25]
