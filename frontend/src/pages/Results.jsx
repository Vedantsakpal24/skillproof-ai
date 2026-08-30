import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getVerifiedSkills } from '../services/api';
import { CheckCircle, ArrowRight, ShieldCheck, ChevronRight } from 'lucide-react';

export default function Results({ userId }) {
  const [verifiedSkills, setVerifiedSkills] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    if (!userId) {
      navigate('/');
      return;
    }
    const fetchData = async () => {
      try {
        const verified = await getVerifiedSkills(userId);
        setVerifiedSkills(verified);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [userId, navigate]);

  if (loading) {
    return <div className="flex h-[60vh] items-center justify-center font-medium text-gray-500 animate-pulse">Loading verified profile...</div>;
  }

  return (
    <div className="max-w-3xl mx-auto mt-10 animate-fade-in-up">
      <div className="text-center mb-10">
        <div className="w-16 h-16 bg-emerald-100 rounded-full flex items-center justify-center mx-auto mb-4 shadow-sm">
          <ShieldCheck className="w-8 h-8 text-emerald-600" />
        </div>
        <h2 className="text-4xl font-extrabold text-gray-900 tracking-tight mb-3">Skill Verification Complete!</h2>
        <p className="text-gray-500 text-lg">Your technical knowledge has been proven. Here are your verified market value scores.</p>
      </div>

      <div className="bg-white p-8 md:p-12 rounded-3xl shadow-sm border border-gray-100">
        <div className="space-y-6 mb-10">
          {verifiedSkills.map((skill, index) => (
            <div key={index} className="p-6 rounded-2xl border border-gray-100 bg-gray-50">
              <div className="flex justify-between items-center mb-4">
                <h3 className="text-xl font-bold text-gray-900">{skill.skill_name}</h3>
                <span className={`px-4 py-1.5 rounded-full text-sm font-bold shadow-sm ${
                  skill.level === 'Advanced' ? 'bg-emerald-100 text-emerald-700' :
                  skill.level === 'Intermediate' ? 'bg-blue-100 text-blue-700' :
                  skill.level === 'Beginner' ? 'bg-amber-100 text-amber-700' : 'bg-gray-100 text-gray-700'
                }`}>
                  {skill.level}
                </span>
              </div>
              
              <div className="w-full bg-gray-200 rounded-full h-3 mb-2 overflow-hidden">
                <div 
                  className={`h-3 rounded-full ${
                    skill.level === 'Advanced' ? 'bg-emerald-500' :
                    skill.level === 'Intermediate' ? 'bg-blue-500' :
                    skill.level === 'Beginner' ? 'bg-amber-500' : 'bg-gray-500'
                  }`}
                  style={{ width: `${Math.max(0, skill.score)}%` }}
                ></div>
              </div>
              <div className="text-right text-sm font-black text-gray-400">
                {Math.round(skill.score)}%
              </div>
            </div>
          ))}
          {verifiedSkills.length === 0 && (
            <div className="text-center py-8 text-gray-500">No skills were successfully verified.</div>
          )}
        </div>

        <button 
          onClick={() => navigate('/dashboard')}
          className="w-full py-4 bg-gray-900 text-white rounded-xl text-lg font-medium hover:bg-gray-800 transition-all shadow-md flex items-center justify-center gap-2"
        >
          Go To Dashboard <ArrowRight className="w-5 h-5" />
        </button>
      </div>
    </div>
  );
}
