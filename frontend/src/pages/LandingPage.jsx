import { useNavigate } from 'react-router-dom';
import { ArrowRight, Briefcase, Target, ListPlus } from 'lucide-react';

export default function LandingPage() {
  const navigate = useNavigate();

  return (
    <div className="flex flex-col items-center mt-16 md:mt-24 px-4">
      {/* Hero Section */}
      <div className="text-center max-w-4xl mx-auto mb-20 animate-fade-in-up">
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-50 border border-blue-100 text-blue-600 text-sm font-semibold mb-8 tracking-wide">
          <Briefcase className="w-4 h-4" />
          Live Career Intelligence
        </div>
        <h1 className="text-5xl md:text-7xl font-extrabold text-gray-900 mb-8 tracking-tight leading-tight">
          Don't just list your skills.<br/>
          <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">
            Prove them.
          </span>
        </h1>
        <p className="text-xl md:text-2xl text-gray-500 mb-12 max-w-2xl mx-auto font-light leading-relaxed">
          Verify your true technical abilities through adaptive testing and get matched instantly with real, live job opportunities.
        </p>
        
        <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
          <button
            onClick={() => navigate('/skills')}
            className="w-full sm:w-auto px-8 py-4 bg-gray-900 text-white rounded-xl text-lg font-medium hover:bg-gray-800 transition-all shadow-lg hover:shadow-xl hover:-translate-y-0.5 flex items-center justify-center gap-2"
          >
            Get Started <ArrowRight className="w-5 h-5" />
          </button>
        </div>
      </div>

      {/* Features Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl w-full">
        <FeatureCard 
          icon={<ListPlus className="w-6 h-6 text-blue-600" />}
          title="1. Claim Your Skills"
          desc="Add your technical skills and languages to start building your personalized professional profile."
        />
        <FeatureCard 
          icon={<Target className="w-6 h-6 text-indigo-600" />}
          title="2. Target a Career"
          desc="Select your dream role. Our engine adapts to ensure you are tested on what truly matters."
        />
        <FeatureCard 
          icon={<Briefcase className="w-6 h-6 text-purple-600" />}
          title="3. Verify & Match"
          desc="Take adaptive quizzes to prove your proficiency and instantly unlock live job matches on your dashboard."
        />
      </div>
    </div>
  );
}

function FeatureCard({ icon, title, desc }) {
  return (
    <div className="bg-white p-8 rounded-2xl border border-gray-100 shadow-sm hover:shadow-md transition-shadow">
      <div className="w-12 h-12 bg-gray-50 rounded-xl flex items-center justify-center mb-6 border border-gray-100">
        {icon}
      </div>
      <h3 className="text-xl font-bold text-gray-900 mb-3">{title}</h3>
      <p className="text-gray-500 leading-relaxed">{desc}</p>
    </div>
  );
}
