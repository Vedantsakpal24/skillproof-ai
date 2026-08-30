import csv
import random

roles = ["Frontend Developer", "Backend Developer", "Full Stack Developer"]
skills_pool = {
    "Frontend Developer": ["HTML", "CSS", "JavaScript", "React", "Next.js", "TypeScript"],
    "Backend Developer": ["Python", "Node.js", "SQL", "PostgreSQL", "MongoDB", "Docker", "FastAPI"],
    "Full Stack Developer": ["JavaScript", "React", "Node.js", "Python", "SQL", "HTML", "CSS", "Docker"]
}

with open("jobs.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["job_id", "job_title", "location", "skills", "description"])
    for i in range(1, 201):
        role = random.choice(roles)
        num_skills = random.randint(3, 5)
        req_skills = random.sample(skills_pool[role], min(num_skills, len(skills_pool[role])))
        writer.writerow([i, role, "Remote", ",".join(req_skills), f"Great opportunity for a {role}"])
