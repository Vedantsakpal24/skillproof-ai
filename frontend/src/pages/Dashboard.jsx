import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { getPersonalizedDashboard } from '../services/api';
import { Briefcase, ShieldCheck, TrendingUp, Target, CheckCircle2, ChevronRight, XCircle } from 'lucide-react';

export default function Dashboard({ userId }) {
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!userId) {
      navigate('/');
      return;
    }

    const fetchData = async () => {
      try {
        const res = await getPersonalizedDashboard(userId);
        setData(res);
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    
    fetchData();
  }, [userId, navigate]);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center h-[60vh]">
        <div className="w-12 h-12 border-4 border-blue-600 rounded-full border-t-transparent animate-spin mb-4"></div>
        <p className="text-gray-500 font-medium animate-pulse">Analyzing Remotive Job Market...</p>
      </div>
    );
  }

  if (!data) {
    return (
      <div className="text-center mt-20">
        <h2 className="text-2xl font-bold text-gray-800">No dashboard data found.</h2>
        <button onClick={() => navigate('/')} className="mt-6 text-blue-600 font-medium hover:underline">
          Return Home
        </button>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto animate-fade-in-up pb-20">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-10 gap-6">
        <div>
          <h1 className="text-4xl font-black text-gray-900 tracking-tight mb-2">Career Dashboard</h1>
          <p className="text-lg text-gray-500 font-medium">Target Role: <span className="text-blue-600 font-bold">{data.career_goal}</span></p>
        </div>
        
        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 text-white px-8 py-4 rounded-2xl shadow-lg border border-blue-700 flex items-center gap-4">
          <Target className="w-8 h-8 text-blue-100" />
          <div>
            <p className="text-xs font-bold tracking-widest text-blue-200 uppercase mb-1">Career Readiness</p>
            <p className="text-3xl font-black">{data.readiness_score || 0}<span className="text-lg font-bold text-blue-200"> / 100</span></p>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="md:col-span-1 space-y-6">
          <div className="bg-white rounded-3xl p-6 border border-gray-100 shadow-sm">
            <h3 className="text-lg font-extrabold text-gray-900 mb-4 flex items-center gap-2">
              <ShieldCheck className="w-5 h-5 text-green-600" /> Verified Skills
            </h3>
            {data.verified_skills && data.verified_skills.length > 0 ? (
              <ul className="space-y-3">
                {data.verified_skills.map((skill, idx) => (
                  <li key={idx} className="flex items-center gap-3 p-3 bg-gray-50 rounded-xl border border-gray-100 font-bold text-gray-700">
                    <CheckCircle2 className="w-5 h-5 text-green-500" /> {skill}
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-gray-500 text-sm p-4 bg-gray-50 rounded-xl">No skills verified yet.</p>
            )}
          </div>
          
          <div className="bg-white rounded-3xl p-6 border border-gray-100 shadow-sm">
            <h3 className="text-lg font-extrabold text-gray-900 mb-4 flex items-center gap-2">
              <TrendingUp className="w-5 h-5 text-purple-600" /> Market Demand
            </h3>
            {Object.keys(data.market_weights || {}).length > 0 ? (
              <div className="space-y-4">
                {Object.entries(data.market_weights).map(([skill, weight], idx) => (
                  <div key={idx}>
                    <div className="flex justify-between text-sm font-bold text-gray-700 mb-1">
                      <span>{skill}</span>
                      <span className="text-purple-600">{weight}%</span>
                    </div>
                    <div className="w-full bg-gray-100 rounded-full h-2">
                      <div className="bg-purple-500 h-2 rounded-full" style={{ width: `${weight}%` }}></div>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-gray-500 text-sm">No market data available.</p>
            )}
          </div>
        </div>

        <div className="md:col-span-2">
          <div className="bg-white rounded-3xl p-6 md:p-8 border border-gray-100 shadow-sm">
            <h3 className="text-2xl font-extrabold text-gray-900 mb-6 flex items-center gap-3">
              <Briefcase className="w-6 h-6 text-gray-700" /> Recommended Job Opportunities
            </h3>
            
            {data.jobs && data.jobs.length > 0 ? (
              <div className="space-y-4">
                {data.jobs.map((job, idx) => (
                  <div key={idx} className="p-5 border-2 border-gray-100 rounded-2xl hover:border-blue-400 hover:shadow-md transition-all group">
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="text-lg font-bold text-gray-900 group-hover:text-blue-700 transition-colors">{job.title}</h4>
                      <span className={`px-3 py-1 rounded-full text-xs font-bold tracking-wider ${job.match_score >= 80 ? 'bg-green-100 text-green-800' : 'bg-yellow-100 text-yellow-800'}`}>
                        {job.match_score}% Match
                      </span>
                    </div>
                    <p className="text-sm text-gray-500 font-medium mb-4">{job.company} &bull; {job.location}</p>
                    
                    <div className="flex flex-wrap gap-2 mb-5">
                      {job.matched_skills && job.matched_skills.map((skill, sIdx) => (
                        <span key={sIdx} className="px-3 py-1 rounded-lg text-xs font-bold bg-green-50 text-green-700 border border-green-200 flex items-center gap-1">
                          <CheckCircle2 className="w-3 h-3"/> {skill}
                        </span>
                      ))}
                      {job.partial_skills && job.partial_skills.map((skill, sIdx) => (
                        <span key={sIdx} className="px-3 py-1 rounded-lg text-xs font-bold bg-amber-50 text-amber-700 border border-amber-200">
                          {skill}
                        </span>
                      ))}
                      {job.missing_skills && job.missing_skills.slice(0, 3).map((skill, sIdx) => (
                        <span key={sIdx} className="px-3 py-1 rounded-lg text-xs font-bold bg-gray-50 text-gray-500 border border-gray-200 flex items-center gap-1">
                          <XCircle className="w-3 h-3"/> {skill}
                        </span>
                      ))}
                      {job.missing_skills && job.missing_skills.length > 3 && (
                         <span className="px-3 py-1 rounded-lg text-xs font-bold bg-gray-50 text-gray-400 border border-gray-100">
                           +{job.missing_skills.length - 3} more
                         </span>
                      )}
                    </div>
                    
                    <a 
                      href={job.job_url} 
                      target="_blank" 
                      rel="noreferrer"
                      className="inline-flex items-center text-sm font-bold text-blue-600 hover:text-blue-800 transition-colors"
                    >
                      View on Remotive <ChevronRight className="w-4 h-4 ml-1" />
                    </a>
                  </div>
                ))}
              </div>
            ) : (
              <div className="text-center p-12 bg-gray-50 rounded-2xl border-2 border-dashed border-gray-200">
                <Target className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                <h4 className="text-lg font-bold text-gray-900 mb-2">No Matches Found Yet</h4>
                <p className="text-gray-500 font-medium max-w-md mx-auto">
                  Continue taking skill assessments to unlock personalized job recommendations from the Remotive network.
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
