import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { setTargetRole, submitManualSkills } from '../services/api';
import { ArrowRight, Code2, Database, Briefcase, Paintbrush, Shield, BarChart, Target } from 'lucide-react';

const ROLES = [
  {
    category: "Software Development",
    icon: <Code2 className="w-6 h-6" />,
    roles: [
      { id: 'frontend', title: 'Frontend Developer', desc: 'React, Vue, UI Architecture', req: ["JavaScript", "React", "HTML", "CSS", "TypeScript"] },
      { id: 'backend', title: 'Backend Developer', desc: 'Node.js, Python, System Design', req: ["Python", "Node.js", "SQL", "Docker", "APIs"] },
      { id: 'fullstack', title: 'Full Stack Developer', desc: 'End-to-end Web Development', req: ["JavaScript", "React", "Node.js", "SQL", "Docker"] }
    ]
  },
  {
    category: "Data & AI",
    icon: <Database className="w-6 h-6" />,
    roles: [
      { id: 'data_analyst', title: 'Data Analyst', desc: 'SQL, Python, Data Visualization', req: ["SQL", "Python", "Excel", "Tableau", "Statistics"] },
      { id: 'data_scientist', title: 'Data Scientist', desc: 'ML, Stats, Pandas, Experimentation', req: ["Python", "SQL", "Pandas", "Statistics", "Machine_Learning"] },
      { id: 'ml_engineer', title: 'Machine Learning Engineer', desc: 'Scikit-learn, PyTorch, MLOps', req: ["Python", "SQL", "Scikit_Learn", "PyTorch", "MLOps"] },
      { id: 'ai_engineer', title: 'AI Engineer', desc: 'LLMs, RAG, Deep Learning', req: ["Python", "Docker", "LLMs", "RAG", "Prompt_Engineering"] },
      { id: 'nlp_engineer', title: 'NLP Engineer', desc: 'Transformers, Embeddings, Hugging Face', req: ["Python", "Transformers", "Embeddings", "Hugging_Face", "PyTorch"] },
      { id: 'cv_engineer', title: 'Computer Vision Engineer', desc: 'OpenCV, YOLO, Object Detection', req: ["Python", "OpenCV", "YOLO", "PyTorch", "Image_Processing"] }
    ]
  },
  {
    category: "Infrastructure & Security",
    icon: <Shield className="w-6 h-6" />,
    roles: [
      { id: 'devops', title: 'DevOps Engineer', desc: 'Docker, AWS, CI/CD, Terraform', req: ["Docker", "Python", "AWS", "CI_CD", "Kubernetes"] },
      { id: 'qa', title: 'QA Tester', desc: 'Automation, Selenium, API Testing', req: ["JavaScript", "Python", "Selenium", "Automation", "API_Testing"] },
      { id: 'cybersecurity', title: 'Cybersecurity Analyst', desc: 'SIEM, Threat Detection, OWASP', req: ["Python", "SQL", "Networking", "Threat_Detection", "OWASP"] }
    ]
  },
  {
    category: "Design",
    icon: <Paintbrush className="w-6 h-6" />,
    roles: [
      { id: 'uiux', title: 'UI/UX Designer', desc: 'Figma, Wireframing, User Research', req: ["HTML", "CSS", "Figma", "User_Research", "Prototyping"] }
    ]
  },
  {
    category: "Business & Strategy",
    icon: <Target className="w-6 h-6" />,
    roles: [
      { id: 'pm', title: 'Product Manager', desc: 'Agile, Roadmap, Stakeholder Mgmt', req: ["Agile", "Analytics", "Roadmap_Strategy", "Stakeholder_Management", "User_Stories"] },
      { id: 'marketing', title: 'Digital Marketing Specialist', desc: 'SEO, Google Ads, Analytics', req: ["SEO", "Google_Ads", "Analytics", "Content_Strategy", "Social_Media"] },
      { id: 'sales', title: 'Sales Representative / Business Development', desc: 'CRM, Negotiation, Pipeline', req: ["CRM", "Communication", "Negotiation", "Lead_Generation", "B2B_Sales"] }
    ]
  }
];

export default function TargetRole({ userId, claimedSkills = [], setClaimedSkills }) {
  const [selectedRoleObj, setSelectedRoleObj] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleContinue = async () => {
    if (!selectedRoleObj) return;
    setLoading(true);
    try {
      await setTargetRole(userId, selectedRoleObj.title);
      
      // Do not force career required skills. Only test what the user manually selected.
      if (claimedSkills && claimedSkills.length > 0) {
         navigate(`/test/${claimedSkills[0]}`);
      } else {
         navigate('/dashboard');
      }
    } catch (err) {
      console.error(err);
      navigate('/dashboard');
    } finally {
      setLoading(false);
    }
  };


  return (
    <div className="max-w-6 mx-auto mt-4 animate-fade-in-up pb-20">
      <div className="text-center mb-10">
        <h2 className="text-3xl font-extrabold text-gray-900 tracking-tight">Select Your Career Path</h2>
        <p className="mt-4 text-lg text-gray-600 max-w-2l mx-auto">
          SkillProof AI will dynamically adjust your assessments, scoring, and market analysis based on the actual skills required for your chosen career.
        </p>
      </div>

      <div className="space-y-12">
        {ROLES.map((group, groupIdx) => (
          <div key={groupIdx} className="bg-white p-8 rounded-3xl shadow-sm border border-gray-100">
            <div className="flex items-center gap-3 mb-6">
              <div className="p-3 bg-blue-50 text-blue-600 rounded-xl">
                {group.icon}
              </div>
              <h3 className="text-xl font-bold text-gray-900">{group.category}</h3>
            </div>
            
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {group.roles.map((role) => (
                <button
                  key={role.id}
                  onClick={() => setSelectedRoleObj(role)}
                  className={`p-6 text-left rounded-2xl border-2 transition-all duration-200 ${
                    selectedRoleObj?.id === role.id 
                      ? 'border-blue-600 bg-blue-50/50 shadow-md transform -translate-y-1' 
                      : 'border-gray-100 hover:border-blue-200 hover:bg-gray-50'
                  }`}
                >
                  <div className="flex items-center justify-between mb-2">
                    <h4 className={`text-lg font-bold ${selectedRoleObj?.id === role.id ? 'text-blue-900' : 'text-gray-900'}`}>
                      {role.title}
                    </h4>
                    {selectedRoleObj?.id === role.id && (
                      <div className="w-3 h-3 bg-blue-600 rounded-full shadow-sm animate-pulse"></div>
                    )}
                  </div>
                  <p className="text-sm text-gray-500 font-medium leading-relaxed mb-3">{role.desc}</p>
                  <div className="flex flex-wrap gap-1">
                    {role.req.map(s => (
                       <span key={s} className="px-2 py-1 bg-gray-100 text-gray-600 text-xs font-bold rounded-md">{s}</span>
                    ))}
                  </div>
                </button>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div className="mt-12 flex justify-center sticky bottom-8 z-10">
        <button
          onClick={handleContinue}
          disabled={!selectedRoleObj || loading}
          className="px-10 py-4 bg-gray-900 text-white rounded-xl text-lg font-medium hover:bg-gray-800 transition-all shadow-xl disabled:opacity-50 disabled:hover:bg-gray-900 flex items-center gap-2"
        >
          {loading ? 'Generating Assessments...' : 'Confirm Career Path'} 
          {!loading && <ArrowRight className="w-5 h-5"/>}
        </button>
      </div>
    </div>
  );
}
