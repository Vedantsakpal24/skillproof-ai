import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { submitManualSkills } from '../services/api';
import { CheckCircle2, Loader2, Plus, X } from 'lucide-react';

export default function UploadResume({ setUserId, setClaimedSkills }) {
  const [skills, setSkills] = useState([]);
  const [currentSkill, setCurrentSkill] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleAddSkill = (e) => {
    e.preventDefault();
    if (currentSkill.trim() && !skills.includes(currentSkill.trim())) {
      setSkills([...skills, currentSkill.trim()]);
      setCurrentSkill("");
    }
  };

  const handleRemoveSkill = (skillToRemove) => {
    setSkills(skills.filter(s => s !== skillToRemove));
  };

  const handleSubmit = async () => {
    if (skills.length === 0) return;
    setLoading(true);
    try {
      const res = await submitManualSkills(skills);
      setUserId(res.id);
      setClaimedSkills(res.claimed_skills.map(s => s.skill_name));
      navigate('/career-selection');
    } catch (err) {
      console.error(err);
      alert("Failed to save skills. Make sure the backend is running.");
      setLoading(false);
    }
  };

  const commonSkills = [
    'HTML', 'API_Testing', 'Lead_Generation', 'Kubernetes', 'CSS', 'Hugging_Face', 'Image_Processing', 
    'Roadmap_Strategy', 'Tableau', 'Analytics', 'Python', 'YOLO', 'B2B_Sales', 'Docker', 'Agile', 'Embeddings', 
    'User_Research', 'PyTorch', 'Transformers', 'Google_Ads', 'JavaScript', 'APIs', 'Pandas', 'Content_Strategy', 
    'Machine_Learning', 'LLMs', 'Prompt_Engineering', 'Threat_Detection', 'CRM', 'OpenCV', 'Excel', 'AWS', 
    'Selenium', 'TypeScript', 'SQL', 'Communication', 'Negotiation', 'Figma', 'Prototyping', 'React', 'MLOps', 
    'Statistics', 'Social_Media', 'RAG', 'OWASP', 'CI_CD', 'User_Stories', 'SEO', 'Node.js', 'Networking', 
    'Scikit_Learn', 'Stakeholder_Management', 'Automation'
  ].sort();

  const handleAddCommon = (skill) => {
    if (!skills.includes(skill)) {
      setSkills([...skills, skill]);
    }
  };

  return (
    <div className="max-w-2xl mx-auto mt-10 animate-fade-in-up">
      <div className="text-center mb-10">
        <h2 className="text-3xl font-extrabold text-gray-900 tracking-tight mb-3">Select Your Skills</h2>
        <p className="text-gray-500 text-lg">List the technical skills you want to verify.</p>
      </div>

      <div className="bg-white p-8 md:p-12 rounded-3xl shadow-sm border border-gray-100">
        
        <form onSubmit={handleAddSkill} className="mb-8">
          <div className="flex gap-3">
            <input 
              type="text" 
              value={currentSkill}
              onChange={(e) => setCurrentSkill(e.target.value)}
              placeholder="Search or add skills..." 
              className="flex-1 p-4 bg-gray-50 border border-gray-200 rounded-xl text-gray-700 focus:ring-2 focus:ring-blue-500 focus:outline-none transition-all"
            />
            <button 
              type="submit"
              disabled={!currentSkill.trim()}
              className="px-6 py-4 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-700 transition disabled:opacity-50 flex items-center gap-2"
            >
              <Plus className="w-5 h-5" /> Add
            </button>
          </div>
        </form>

        <div className="mb-10">
          <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-4">Popular Skills:</h3>
          <div className="flex flex-wrap gap-2">
            {commonSkills.map(skill => (
              <button 
                key={skill}
                onClick={() => handleAddCommon(skill)}
                disabled={skills.includes(skill)}
                className="px-4 py-2 bg-white border border-gray-200 text-gray-600 rounded-lg text-sm font-medium hover:border-gray-300 hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {skill}
              </button>
            ))}
          </div>
        </div>

        {skills.length > 0 && (
          <div className="mb-8 p-6 bg-gray-50 rounded-2xl border border-gray-200">
            <h3 className="text-sm font-bold text-gray-500 uppercase tracking-wider mb-4">Selected Skills:</h3>
            <div className="flex flex-wrap gap-2">
              {skills.map(skill => (
                <span key={skill} className="px-4 py-2 bg-blue-100 text-blue-800 rounded-lg text-sm font-semibold flex items-center gap-2">
                  {skill}
                  <button onClick={() => handleRemoveSkill(skill)} className="hover:text-red-600 transition-colors ml-1">
                    <X className="w-4 h-4" />
                  </button>
                </span>
              ))}
            </div>
          </div>
        )}

        <button 
          onClick={handleSubmit} 
          disabled={skills.length === 0 || loading}
          className="w-full py-4 bg-gray-900 text-white rounded-xl text-lg font-medium disabled:opacity-50 disabled:cursor-not-allowed hover:bg-gray-800 transition-all shadow-md flex items-center justify-center gap-2"
        >
          {loading ? (
            <><Loader2 className="w-5 h-5 animate-spin" /> Saving...</>
          ) : (
            'Continue'
          )}
        </button>
      </div>
    </div>
  );
}
