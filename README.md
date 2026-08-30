# 🎯 SkillProof AI
*Intelligent Career Opportunity & Skill Verification Platform*

SkillProof AI is a full-stack, local-first capstone project designed to bridge the gap between claimed skills and true market value. Rather than blindly trusting self-reported skills, SkillProof AI verifies a user's technical abilities through adaptive quizzes and multi-language sandbox coding challenges. It then analyzes a local job market dataset to calculate exact Opportunity ROI and recommend the single best next skill to learn.

---

## ✨ Key Features
- **Manual Skill Claiming:** Easily select and input your current technical stack (Python, React, Node.js, SQL, Docker, HTML, CSS, JavaScript).
- **Adaptive Quiz Engine:** A dynamic testing engine that scales difficulty (Easy → Medium → Hard) based on whether you answer correctly.
- **Multi-Language Coding Sandbox:** A secure, local execution environment that runs and validates real code for Python, JavaScript/Node, and SQL via in-memory databases and isolated child processes.
- **Market Demand Analysis:** Parses a local `jobs.csv` dataset to calculate exactly how frequently your skills appear in real job postings.
- **Opportunity Simulator:** A "What-If" engine that temporarily injects a missing skill into your profile to calculate exactly how many *new* jobs you would unlock by learning it.
- **ROI Recommendation:** Recommends the mathematically best next skill to learn based on Opportunity Gain, Market Demand, and Learning Effort.

---

## 🛠️ Tech Stack
- **Frontend:** React, Vite, Tailwind CSS v4, Recharts, Monaco Editor, Lucide Icons.
- **Backend:** Python, FastAPI, Uvicorn, SQLAlchemy, SQLite, Pydantic, Pandas.
- **Execution Engine:** Native Python `exec()`, Node.js `child_process`, SQLite `:memory:` database.
- **Deployment:** Docker, Docker Compose, Nginx.

---

## 🚀 Quick Start (Local Development)

### 1. Start the Backend
Requires Python 3.9+ and Node.js (for the JS code runner).
```bash
cd backend
python -m venv venv
source venv/Scripts/activate  # On Windows: .\venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### 2. Start the Frontend
Requires Node.js.
```bash
cd frontend
npm install
npm run dev
```
Navigate to `http://localhost:5173` in your browser.

---

## 🐳 Docker Deployment
You can deploy the entire stack instantly using Docker Compose. The backend container automatically provisions a Python and Node.js environment.

```bash
docker compose up --build -d
```
Access the application at `http://localhost`.

---

## 📂 Project Structure
- `/backend/app/algorithms`: Core intelligence (Market Analyzer, Code Runner, Adaptive Quiz).
- `/backend/app/data`: Local datasets (`jobs.csv`) and JSON question banks.
- `/backend/app/routers`: FastAPI endpoints for UI interaction.
- `/frontend/src/pages`: React UI views (Landing, Target Role, Verification, Dashboard).
- `/frontend/src/services`: API abstraction layer.

---

## 🎓 Capstone Constraints
This project was built with strict MVP constraints:
- **No External LLMs / Paid APIs:** All intelligence is handled by local algorithms, Pandas matching, and lightweight execution sandboxes.
- **Local Data Only:** The job market relies entirely on a localized CSV dataset for reliable offline demonstrations.
# skillproof-ai
