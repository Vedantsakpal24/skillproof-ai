from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship
from ..database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    target_role = Column(String, nullable=True)
    
    claimed_skills = relationship("ClaimedSkill", back_populates="user", cascade="all, delete-orphan")
    verified_skills = relationship("VerifiedSkill", back_populates="user", cascade="all, delete-orphan")

class ClaimedSkill(Base):
    __tablename__ = "claimed_skills"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    skill_name = Column(String, index=True)
    
    user = relationship("User", back_populates="claimed_skills")

class VerifiedSkill(Base):
    __tablename__ = "verified_skills"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    skill_name = Column(String, index=True)
    score = Column(Float)
    level = Column(String)
    
    user = relationship("User", back_populates="verified_skills")
