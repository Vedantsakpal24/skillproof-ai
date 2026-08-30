import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import UploadResume from './pages/UploadResume';
import TargetRole from './pages/TargetRole';
import Verification from './pages/Verification';
import Results from './pages/Results';
import Dashboard from './pages/Dashboard';
import { ShieldCheck, UserCircle, LayoutDashboard, LogOut } from 'lucide-react';

function App() {
  const [userId, setUserId] = useState(() => {
    return localStorage.getItem('userId') || null;
  });
  const [claimedSkills, setClaimedSkills] = useState(() => {
    const saved = localStorage.getItem('claimedSkills');
    if (saved) {
      try { return JSON.parse(saved); } catch (e) { return []; }
    }
    return [];
  });

  useEffect(() => {
    if (userId) localStorage.setItem('userId', userId);
    else localStorage.removeItem('userId');
  }, [userId]);

  useEffect(() => {
    localStorage.setItem('claimedSkills', JSON.stringify(claimedSkills));
  }, [claimedSkills]);

  return (
    <Router>
      <div className="min-h-screen bg-gray-50/50 text-gray-900 font-sans selection:bg-blue-100 selection:text-blue-900">
        <header className="sticky top-0 z-50 bg-white/80 backdrop-blur-lg border-b border-gray-200/50 shadow-sm print:hidden">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex justify-between items-center">
            <Link to={userId ? "/dashboard" : "/"} className="flex items-center gap-2 group">
              <div className="bg-blue-600 p-2 rounded-lg group-hover:bg-blue-700 transition-colors">
                <ShieldCheck className="text-white w-5 h-5" />
              </div>
              <span className="text-xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-gray-900 to-gray-600 tracking-tight">
                SkillProof <span className="font-light">AI</span>
              </span>
            </Link>

            {userId && (
              <nav className="flex items-center gap-6">
                <Link to="/dashboard" className="flex items-center gap-2 text-sm font-medium text-gray-600 hover:text-blue-600 transition-colors">
                  <LayoutDashboard className="w-4 h-4" />
                  Dashboard
                </Link>
                <div className="h-4 w-px bg-gray-300"></div>
                <div className="flex items-center gap-2 text-sm font-medium text-gray-700">
                  <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-100 to-purple-100 border border-blue-200 flex items-center justify-center">
                    <UserCircle className="w-5 h-5 text-blue-600" />
                  </div>
                  User #{userId}
                </div>
                <button 
                  onClick={() => setUserId(null)}
                  className="text-gray-400 hover:text-red-500 transition-colors"
                  title="Sign out"
                >
                  <LogOut className="w-4 h-4" />
                </button>
              </nav>
            )}
          </div>
        </header>
        
        <main className="max-w-7xl mx-auto py-10 px-4 sm:px-6 lg:px-8">
          <Routes>
            <Route path="/" element={<LandingPage setUserId={setUserId} setClaimedSkills={setClaimedSkills} />} />
            <Route path="/skills" element={<UploadResume userId={userId} setUserId={setUserId} setClaimedSkills={setClaimedSkills} />} />
            <Route path="/career-selection" element={<TargetRole userId={userId} claimedSkills={claimedSkills} setClaimedSkills={setClaimedSkills} />} />
            <Route path="/test/:skill" element={<Verification userId={userId} claimedSkills={claimedSkills} />} />
            <Route path="/results" element={<Results userId={userId} />} />
            <Route path="/dashboard" element={<Dashboard userId={userId} />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
