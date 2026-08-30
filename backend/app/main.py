from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import resume, skills, verifications, market, recommendations, demo, dashboard

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SkillProof AI")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(resume.router, prefix="/api/resume", tags=["Resume"])
app.include_router(skills.router, prefix="/api/skills", tags=["Skills"])
app.include_router(verifications.router, prefix="/api/verifications", tags=["Verifications"])
app.include_router(market.router, prefix="/api/market", tags=["Market"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["Recommendations"])
app.include_router(demo.router, prefix="/api/demo", tags=["Demo"])
app.include_router(dashboard.router, prefix="/api/dashboard", tags=["Dashboard"])

@app.get("/")
def read_root():
    return {"message": "Welcome to SkillProof AI Backend"}
