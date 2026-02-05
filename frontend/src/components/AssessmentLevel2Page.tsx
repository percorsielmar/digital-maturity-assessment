import React, { useEffect, useState, useRef } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  ChevronLeft, 
  ChevronRight, 
  Check, 
  Loader2,
  Home,
  HelpCircle
} from 'lucide-react';
import { questionsLevel2Api, assessmentsApi } from '../api';
import { Level2Question } from '../types';

interface Level2Answer {
  question_id: number;
  value: string | string[];
}

const AssessmentLevel2Page: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [questions, setQuestions] = useState<Level2Question[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Map<number, Level2Answer>>(new Map());
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [showHint, setShowHint] = useState(false);
  const answersRef = useRef<Map<number, Level2Answer>>(new Map());

  useEffect(() => {
    loadQuestions();
  }, []);

  useEffect(() => {
    answersRef.current = answers;
  }, [answers]);

  useEffect(() => {
    setShowHint(false);
  }, [currentIndex]);

  const loadQuestions = async () => {
    try {
      const data = await questionsLevel2Api.getQuestions();
      setQuestions(data.questions);
      
      // Load saved progress
      if (id) {
        try {
          const assessment = await assessmentsApi.getById(parseInt(id));
          if (assessment.responses?.answers && assessment.status === 'in_progress') {
            const savedAnswers = new Map<number, Level2Answer>();
            for (const ans of assessment.responses.answers) {
              savedAnswers.set(ans.question_id, {
                question_id: ans.question_id,
                value: (ans as any).value || ans.selected_option?.toString() || ''
              });
            }
            setAnswers(savedAnswers);
          }
        } catch (e) {
          console.log('No saved progress found');
        }
      }
    } catch (error) {
      console.error('Error loading questions:', error);
      alert('Devi completare almeno un assessment di livello 1 prima di accedere al livello 2');
      navigate('/dashboard');
    } finally {
      setLoading(false);
    }
  };

  const currentQuestion = questions[currentIndex];
  const progress = questions.length > 0 ? ((currentIndex + 1) / questions.length) * 100 : 0;

  // Check if question should be shown based on conditional
  const shouldShowQuestion = (question: Level2Question): boolean => {
    if (!question.conditional) return true;
    const condAnswer = answers.get(question.conditional.question_id);
    if (!condAnswer) return false;
    const value = Array.isArray(condAnswer.value) ? condAnswer.value : [condAnswer.value];
    return value.includes(question.conditional.value);
  };

  const handleTextChange = (value: string) => {
    const newAnswers = new Map(answers);
    newAnswers.set(currentQuestion.id, {
      question_id: currentQuestion.id,
      value: value
    });
    setAnswers(newAnswers);
    autoSave(newAnswers);
  };

  const handleSelectChange = (value: string) => {
    const newAnswers = new Map(answers);
    newAnswers.set(currentQuestion.id, {
      question_id: currentQuestion.id,
      value: value
    });
    setAnswers(newAnswers);
    autoSave(newAnswers);
  };

  const handleMultiSelectChange = (value: string, checked: boolean) => {
    const newAnswers = new Map(answers);
    const current = answers.get(currentQuestion.id);
    let values: string[] = [];
    
    if (current && Array.isArray(current.value)) {
      values = [...current.value];
    }
    
    if (checked) {
      if (!values.includes(value)) {
        values.push(value);
      }
    } else {
      values = values.filter(v => v !== value);
    }
    
    newAnswers.set(currentQuestion.id, {
      question_id: currentQuestion.id,
      value: values
    });
    setAnswers(newAnswers);
    autoSave(newAnswers);
  };

  const autoSave = async (newAnswers: Map<number, Level2Answer>) => {
    if (!id) return;
    try {
      const answersArray = Array.from(newAnswers.values()).map(a => ({
        question_id: a.question_id,
        selected_option: 0,
        value: a.value,
        notes: ''
      }));
      await assessmentsApi.saveProgress(parseInt(id), answersArray as any);
    } catch (error) {
      console.error('Error auto-saving:', error);
    }
  };

  const handleNext = () => {
    let nextIndex = currentIndex + 1;
    while (nextIndex < questions.length && !shouldShowQuestion(questions[nextIndex])) {
      nextIndex++;
    }
    if (nextIndex < questions.length) {
      setCurrentIndex(nextIndex);
    }
  };

  const handlePrev = () => {
    let prevIndex = currentIndex - 1;
    while (prevIndex >= 0 && !shouldShowQuestion(questions[prevIndex])) {
      prevIndex--;
    }
    if (prevIndex >= 0) {
      setCurrentIndex(prevIndex);
    }
  };

  const handleSubmit = async () => {
    if (!id) return;
    
    setSubmitting(true);
    try {
      const answersArray = Array.from(answers.values()).map(a => ({
        question_id: a.question_id,
        selected_option: 0,
        value: a.value,
        notes: ''
      }));
      await assessmentsApi.submit(parseInt(id), answersArray as any);
      navigate(`/report/${id}`);
    } catch (error) {
      console.error('Error submitting assessment:', error);
      alert('Errore durante l\'invio. Riprova.');
    } finally {
      setSubmitting(false);
    }
  };

  const getCurrentAnswer = () => {
    return answers.get(currentQuestion?.id);
  };

  const isCurrentAnswered = () => {
    if (!currentQuestion) return false;
    const answer = getCurrentAnswer();
    if (!answer) return false;
    if (Array.isArray(answer.value)) {
      return answer.value.length > 0;
    }
    return answer.value !== '';
  };

  const visibleQuestions = questions.filter(shouldShowQuestion);
  const isLastQuestion = currentIndex === questions.length - 1 || 
    visibleQuestions.indexOf(currentQuestion) === visibleQuestions.length - 1;
  
  const requiredAnswered = visibleQuestions
    .filter(q => q.required)
    .every(q => {
      const ans = answers.get(q.id);
      if (!ans) return false;
      if (Array.isArray(ans.value)) return ans.value.length > 0;
      return ans.value !== '';
    });

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-600 via-primary-700 to-primary-800 flex items-center justify-center">
        <div className="w-16 h-16 border-4 border-white/30 border-t-white rounded-full animate-spin" />
      </div>
    );
  }

  if (!currentQuestion || !shouldShowQuestion(currentQuestion)) {
    handleNext();
    return null;
  }

  const currentCategory = currentQuestion.category;

  return (
    <div className="min-h-screen bg-gradient-to-br from-green-600 via-green-700 to-green-800">
      <header className="bg-white/10 backdrop-blur-sm">
        <div className="max-w-4xl mx-auto px-4 py-4 flex items-center justify-between">
          <button
            onClick={() => navigate('/dashboard')}
            className="flex items-center gap-2 text-white/80 hover:text-white transition-colors"
          >
            <Home className="w-5 h-5" />
            <span className="hidden sm:inline">Dashboard</span>
          </button>
          <div className="text-center">
            <h1 className="text-white font-semibold">Assessment Livello 2</h1>
            <p className="text-white/70 text-sm">{currentCategory}</p>
          </div>
          <div className="text-white/80 text-sm">
            {currentIndex + 1} / {questions.length}
          </div>
        </div>
        <div className="h-1 bg-white/20">
          <div 
            className="h-full bg-white transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8">
        <div className="bg-white rounded-2xl shadow-2xl overflow-hidden">
          <div className="p-6 sm:p-8">
            <div className="flex items-start justify-between gap-4 mb-6">
              <div className="flex-1">
                <span className="text-sm text-green-600 font-medium">{currentQuestion.code}</span>
                <h2 className="text-xl sm:text-2xl font-bold text-gray-800 mt-1">
                  {currentQuestion.text}
                  {currentQuestion.required && <span className="text-red-500 ml-1">*</span>}
                </h2>
              </div>
              {currentQuestion.hint && (
                <button
                  onClick={() => setShowHint(!showHint)}
                  className={`p-2 rounded-full transition-colors ${showHint ? 'bg-green-100 text-green-600' : 'text-gray-400 hover:text-green-600 hover:bg-green-50'}`}
                >
                  <HelpCircle className="w-6 h-6" />
                </button>
              )}
            </div>

            {showHint && currentQuestion.hint && (
              <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-xl">
                <div className="flex items-start gap-3">
                  <HelpCircle className="w-5 h-5 text-green-600 flex-shrink-0 mt-0.5" />
                  <p className="text-sm text-green-800">{currentQuestion.hint}</p>
                </div>
                <button
                  onClick={() => setShowHint(false)}
                  className="mt-2 text-xs text-green-600 hover:text-green-700"
                >
                  Chiudi
                </button>
              </div>
            )}

            <div className="space-y-3">
              {currentQuestion.type === 'text' && (
                <input
                  type="text"
                  value={(getCurrentAnswer()?.value as string) || ''}
                  onChange={(e) => handleTextChange(e.target.value)}
                  className="w-full px-4 py-3 border-2 border-gray-200 rounded-xl focus:border-green-500 focus:ring-2 focus:ring-green-200 transition-all"
                  placeholder="Inserisci la tua risposta..."
                />
              )}

              {currentQuestion.type === 'select' && currentQuestion.options && (
                <div className="space-y-2">
                  {currentQuestion.options.map((option, idx) => (
                    <button
                      key={idx}
                      onClick={() => handleSelectChange(option.value)}
                      className={`w-full p-4 text-left rounded-xl border-2 transition-all ${
                        getCurrentAnswer()?.value === option.value
                          ? 'border-green-500 bg-green-50 text-green-800'
                          : 'border-gray-200 hover:border-green-300 hover:bg-green-50/50'
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        <div className={`w-5 h-5 rounded-full border-2 flex items-center justify-center ${
                          getCurrentAnswer()?.value === option.value
                            ? 'border-green-500 bg-green-500'
                            : 'border-gray-300'
                        }`}>
                          {getCurrentAnswer()?.value === option.value && (
                            <Check className="w-3 h-3 text-white" />
                          )}
                        </div>
                        <span className="text-sm">{option.text}</span>
                      </div>
                    </button>
                  ))}
                </div>
              )}

              {currentQuestion.type === 'multiselect' && currentQuestion.options && (
                <div className="space-y-2">
                  {currentQuestion.options.map((option, idx) => {
                    const currentValues = (getCurrentAnswer()?.value as string[]) || [];
                    const isChecked = currentValues.includes(option.value);
                    return (
                      <button
                        key={idx}
                        onClick={() => handleMultiSelectChange(option.value, !isChecked)}
                        className={`w-full p-4 text-left rounded-xl border-2 transition-all ${
                          isChecked
                            ? 'border-green-500 bg-green-50 text-green-800'
                            : 'border-gray-200 hover:border-green-300 hover:bg-green-50/50'
                        }`}
                      >
                        <div className="flex items-center gap-3">
                          <div className={`w-5 h-5 rounded border-2 flex items-center justify-center ${
                            isChecked
                              ? 'border-green-500 bg-green-500'
                              : 'border-gray-300'
                          }`}>
                            {isChecked && (
                              <Check className="w-3 h-3 text-white" />
                            )}
                          </div>
                          <span className="text-sm">{option.text}</span>
                        </div>
                      </button>
                    );
                  })}
                </div>
              )}
            </div>
          </div>

          <div className="px-6 sm:px-8 pb-6 sm:pb-8 flex items-center justify-between gap-4">
            <button
              onClick={handlePrev}
              disabled={currentIndex === 0}
              className="flex items-center gap-2 px-6 py-3 text-gray-600 hover:text-gray-800 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
            >
              <ChevronLeft className="w-5 h-5" />
              Precedente
            </button>

            {isLastQuestion ? (
              <button
                onClick={handleSubmit}
                disabled={!requiredAnswered || submitting}
                className="flex items-center gap-2 px-8 py-3 bg-green-600 text-white rounded-xl font-semibold hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {submitting ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Elaborazione...
                  </>
                ) : (
                  <>
                    <Check className="w-5 h-5" />
                    Completa Assessment
                  </>
                )}
              </button>
            ) : (
              <button
                onClick={handleNext}
                disabled={currentQuestion.required && !isCurrentAnswered()}
                className="flex items-center gap-2 px-8 py-3 bg-green-600 text-white rounded-xl font-semibold hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                Successiva
                <ChevronRight className="w-5 h-5" />
              </button>
            )}
          </div>
        </div>

        <div className="mt-6 flex justify-center gap-1 flex-wrap">
          {questions.map((q, index) => (
            <button
              key={index}
              onClick={() => setCurrentIndex(index)}
              className={`w-3 h-3 rounded-full transition-all ${
                index === currentIndex
                  ? 'bg-white scale-125'
                  : answers.has(q.id)
                  ? 'bg-white/60'
                  : 'bg-white/30'
              } ${!shouldShowQuestion(q) ? 'opacity-30' : ''}`}
            />
          ))}
        </div>
      </main>
    </div>
  );
};

export default AssessmentLevel2Page;
