import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { startVerification, submitQuizAnswer } from '../services/api';
import { CheckCircle, XCircle, Brain, Target, Code2, BugPlay, ArrowRight } from 'lucide-react';
import Editor from '@monaco-editor/react';

export default function Verification({ userId, claimedSkills }) {
  const { skill } = useParams();
  const navigate = useNavigate();

  const [phase, setPhase] = useState('loading'); // loading, test, result
  const [session, setSession] = useState(null);
  const [question, setQuestion] = useState(null);
  const [feedback, setFeedback] = useState(null);
  const [runResult, setRunResult] = useState(null);
  const [progress, setProgress] = useState('1/23');
  const [codeValue, setCodeValue] = useState('');
  const [submitting, setSubmitting] = useState(false);

  const handleNextSkill = () => {
    const currentIndex = claimedSkills.indexOf(skill);
    if (currentIndex !== -1 && currentIndex < claimedSkills.length - 1) {
      setPhase('loading');
      navigate(`/test/${claimedSkills[currentIndex + 1]}`);
    } else {
      navigate('/dashboard');
    }
  };

  useEffect(() => {
    const init = async () => {
      try {
        const res = await startVerification(userId, skill);
        setSession(res.session_id);
        setQuestion(res.question);
        if (res.question?.default_code) setCodeValue(res.question.default_code);
        setProgress(`1/${res.total_questions}`);
        setPhase('test');
      } catch (err) {
        console.error(err);
        navigate('/dashboard'); 
      }
    };
    init();
  }, [userId, skill, navigate]);

  const handleQuizSubmit = async (optionIndex) => {
    try {
      setSubmitting(true);
      const res = await submitQuizAnswer(session, question.id, optionIndex !== null ? optionIndex : 0);
      
      setFeedback(res.result);
      
      setTimeout(() => {
        setFeedback(null);
        setSubmitting(false);
        if (res.phase === 'result') {
          setRunResult(res);
          setPhase('result');
        } else {
          setQuestion(res.next_question);
          if (res.next_question?.default_code) {
             setCodeValue(res.next_question.default_code);
          } else {
             setCodeValue('');
          }
          if (res.progress) setProgress(res.progress);
        }
      }, 2500);
    } catch (err) {
      console.error(err);
      setSubmitting(false);
    }
  };

  if (phase === 'loading') {
    return (
      <div className="flex flex-col items-center justify-center h-[60vh]">
        <div className="relative">
          <div className="w-16 h-16 border-4 border-gray-100 rounded-full"></div>
          <div className="w-16 h-16 border-4 border-blue-600 rounded-full border-t-transparent animate-spin absolute top-0"></div>
        </div>
        <p className="mt-6 text-gray-500 font-medium animate-pulse">Initializing Career-Aware Engine...</p>
      </div>
    );
  }

  if (phase === 'test') {
    const isScenario = question?.question_type === 'scenario' || question?.question_type === 'case_study';
    const isCoding = question?.question_type === 'coding';
    const isDebugging = question?.question_type === 'debugging';
    const isCode = isCoding || isDebugging;
    
    return (
      <div className="max-w-4xl mx-auto mt-8 animate-fade-in-up pb-20">
        <div className="bg-white p-8 md:p-12 rounded-3xl shadow-sm border border-gray-100 relative overflow-hidden">
          <div className={`absolute top-0 left-0 w-1.5 h-full ${
             isCoding ? 'bg-gradient-to-b from-purple-500 to-pink-500' : 
             isDebugging ? 'bg-gradient-to-b from-red-500 to-orange-500' : 
             isScenario ? 'bg-gradient-to-b from-amber-400 to-orange-500' : 
             'bg-gradient-to-b from-blue-500 to-indigo-500'
          }`}></div>
          
          <div className="flex justify-between items-center mb-8 relative z-10">
            <div className="flex items-center gap-3">
              {isCoding ? <Code2 className="w-8 h-8 text-purple-600" /> : 
               isDebugging ? <BugPlay className="w-8 h-8 text-red-600" /> : 
               isScenario ? <Target className="w-8 h-8 text-amber-500" /> : 
               <Brain className="w-8 h-8 text-blue-600" />}
              <h2 className="text-2xl font-bold text-gray-900 capitalize flex items-center gap-2">
                {skill} 
                <span className="text-gray-400 font-medium text-lg">
                  ({isCoding ? 'Sandbox' : isDebugging ? 'Debugging' : isScenario ? 'Scenario' : 'Concept'})
                </span>
              </h2>
            </div>
            
            <div className="flex items-center gap-3">
                <span className="text-sm font-bold text-gray-400 tracking-widest uppercase">{progress}</span>
                <span className={`px-4 py-1.5 rounded-full text-xs font-bold tracking-wider uppercase shadow-sm border
                ${question?.difficulty === 'Hard' ? 'bg-red-50 text-red-600 border-red-100' : 
                  question?.difficulty === 'Medium' ? 'bg-amber-50 text-amber-600 border-amber-100' : 
                  'bg-emerald-50 text-emerald-600 border-emerald-100'}`}>
                Level: {question?.difficulty}
              </span>
            </div>
          </div>

          <div className="mb-6 relative z-10">
            <p className="text-xl md:text-2xl font-medium text-gray-800 leading-relaxed whitespace-pre-wrap">
              {question?.question}
            </p>
          </div>
          
          {isCode ? (
            <div className="relative z-10 mb-8 border rounded-xl overflow-hidden shadow-sm">
               <Editor 
                 key={question?.id}
                 height="350px"
                 defaultLanguage="javascript"
                 value={codeValue}
                 onChange={(val) => setCodeValue(val || '')}
                 theme="vs-dark"
                 options={{ minimap: { enabled: false }, fontSize: 14 }}
               />
               <div className="p-4 bg-gray-50 border-t flex justify-end">
                  <button
                    onClick={() => handleQuizSubmit(null)}
                    disabled={submitting || !!feedback}
                    className="px-6 py-2.5 bg-gray-900 text-white rounded-lg font-medium hover:bg-gray-800 transition-all disabled:opacity-50 flex items-center gap-2"
                  >
                     <Code2 className="w-4 h-4" /> Run & Submit Code
                  </button>
               </div>
            </div>
          ) : (
            <div className="space-y-3 relative z-10">
              {question?.options?.map((opt, idx) => (
                <button
                  key={idx}
                  disabled={!!feedback || submitting}
                  onClick={() => handleQuizSubmit(idx)}
                  className="w-full text-left px-6 py-5 border border-gray-200 rounded-2xl hover:border-blue-400 hover:bg-blue-50 hover:shadow-sm transition-all disabled:opacity-50 disabled:hover:border-gray-200 disabled:hover:bg-white text-lg font-medium text-gray-700 group"
                >
                  <div className="flex items-center">
                    <span className="w-8 h-8 rounded-lg bg-gray-100 text-gray-500 flex items-center justify-center mr-4 text-sm font-bold group-hover:bg-blue-200 group-hover:text-blue-700 transition-colors shrink-0">
                      {String.fromCharCode(65 + idx)}
                    </span>
                    <span>{opt}</span>
                  </div>
                </button>
              ))}
            </div>
          )}

          {feedback && (
            <div className={`mt-8 p-6 rounded-2xl animate-fade-in-up border ${feedback.correct ? 'bg-emerald-50/80 border-emerald-200' : 'bg-red-50/80 border-red-200'}`}>
              <div className="flex items-center gap-3 mb-2">
                {feedback.correct ? <CheckCircle className="text-emerald-600 w-6 h-6" /> : <XCircle className="text-red-600 w-6 h-6" />}
                <span className={`font-bold text-lg ${feedback.correct ? 'text-emerald-800' : 'text-red-800'}`}>
                  {isCode 
                    ? 'Code execution simulated successfully. Moving to next challenge...' 
                    : (feedback.correct ? 'Correct! Moving to next question...' : 'Incorrect. Moving to next question...')
                  }
                </span>
              </div>
              {!isCode && !feedback.correct && feedback.correct_answer_text && (
                <p className="text-md font-bold text-red-900 mb-2">
                  Correct Answer: <span className="font-semibold text-red-800">{feedback.correct_answer_text}</span>
                </p>
              )}
            </div>
          )}
        </div>
      </div>
    );
  }

  if (phase === 'result') {
    return (
      <div className="max-w-2xl mx-auto mt-16 animate-fade-in-up">
        <div className="bg-white p-12 rounded-3xl shadow-sm border border-gray-100 text-center relative overflow-hidden">
          <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
            <CheckCircle className="w-10 h-10 text-green-600" />
          </div>
          
          <h2 className="text-3xl font-extrabold mb-8 text-gray-900 tracking-tight">Assessment Complete!</h2>
          
          <div className="flex justify-center items-center gap-6 mb-12">
            <div className="flex-1 p-6 bg-gradient-to-b from-blue-50 to-white rounded-2xl border border-blue-100 shadow-sm">
              <p className="text-blue-600 text-xs mb-2 uppercase tracking-widest font-bold">Verified Score</p>
              <p className="text-6xl font-black text-gray-900">{Math.round(runResult?.score || 0)}</p>
              <p className="text-sm text-gray-500 mt-1">out of 100</p>
            </div>
            <div className="flex-1 p-6 bg-gradient-to-b from-purple-50 to-white rounded-2xl border border-purple-100 shadow-sm">
              <p className="text-purple-600 text-xs mb-2 uppercase tracking-widest font-bold">Assessed Level</p>
              <p className="text-3xl font-black text-gray-900 mt-3">{runResult?.level}</p>
            </div>
          </div>
          
          <button 
            onClick={handleNextSkill}
            className="w-full py-4 bg-gray-900 text-white rounded-xl text-lg font-medium hover:bg-gray-800 transition-all shadow-md flex items-center justify-center gap-2"
          >
            {claimedSkills.indexOf(skill) < claimedSkills.length - 1 ? (
              <>Verify Next Skill <ArrowRight className="w-5 h-5"/></>
            ) : (
              <>Go to Personalized Dashboard <ArrowRight className="w-5 h-5"/></>
            )}
          </button>
        </div>
      </div>
    );
  }
}
