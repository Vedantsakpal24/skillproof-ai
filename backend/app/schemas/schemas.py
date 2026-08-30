from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    id: Optional[int] = None

class UserRoleUpdate(BaseModel):
    target_role: str

class ClaimedSkillBase(BaseModel):
    skill_name: str

class VerifiedSkillBase(BaseModel):
    skill_name: str
    score: float
    level: str

class UserResponse(BaseModel):
    id: int
    target_role: Optional[str] = None
    claimed_skills: List[ClaimedSkillBase] = []
    verified_skills: List[VerifiedSkillBase] = []
    
    class Config:
        from_attributes = True

class QuizAnswer(BaseModel):
    question_id: str
    selected_option: int

class CodeSubmission(BaseModel):
    task_id: Optional[int] = None
    code: str

class SimulationRequest(BaseModel):
    skill_name: str

class ManualSkillsRequest(BaseModel):
    skills: List[str]
