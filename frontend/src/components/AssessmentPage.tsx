import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  ChevronLeft, 
  ChevronRight, 
  Check, 
  Loader2,
  Home
} from 'lucide-react';
import { questionsApi, assessmentsApi } from '../api';
import { Question, Answer } from '../types';

const AssessmentPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Map<number, Answer>>(new Map());
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [categories, setCategories] = useState<string[]>([]);

  useEffect(() => {
    loadQuestions();
  }, []);

  const loadQuestions = async () => {
    try {
      const data = await questionsApi.getQuestions();
      setQuestions(data);
      const uniqueCategories = [...new Set(data.map(q => q.category))];
      setCategories(uniqueCategories);
    } catch (error) {
      console.error('Error loading questions:', error);
    } finally {
      setLoading(false);
    }
  };

  const currentQuestion = questions[currentIndex];
  const progress = ((currentIndex + 1) / questions.length) * 100;

  const handleSelectOption = (optionIndex: number) => {
    const newAnswers = new Map(answers);
    newAnswers.set(currentQuestion.id, {
      question_id: currentQuestion.id,
      selected_option: optionIndex
    });
    setAnswers(newAnswers);
  };

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex(currentIndex + 1);
    }
  };

  const handlePrev = () => {
    if (currentIndex > 0) {
      setCurrentIndex(currentIndex - 1);
    }
  };

  const handleSubmit = async () => {
    if (!id) return;
    
    setSubmitting(true);
    try {
      const answersArray = Array.from(answers.values());
      await assessmentsApi.submit(parseInt(id), answersArray);
      navigate(`/report/${id}`);
    } catch (error) {
      console.error('Error submitting assessment:', error);
      alert('Errore durante l\'invio. Riprova.');
    } finally {
      setSubmitting(false);
    }
  };

  const isLastQuestion = currentIndex === questions.length - 1;
  const currentAnswer = currentQuestion ? answers.get(currentQuestion.id) : undefined;
  const allAnswered = questions.length > 0 && answers.size === questions.length;

  const getCategoryProgress = () => {
    const categoryQuestions = questions.filter(q => q.category === currentQuestion?.category);
    const categoryAnswered = categoryQuestions.filter(q => answers.has(q.id)).length;
    return { answered: categoryAnswered, total: categoryQuestions.length };
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-600 to-primary-900 flex items-center justify-center">
        <div className="w-16 h-16 border-4 border-white border-t-transparent rounded-full animate-spin" />
      </div>
    );
  }

  if (!currentQuestion) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <p className="text-gray-500">Nessuna domanda disponibile</p>
      </div>
    );
  }

  const categoryProgress = getCategoryProgress();

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-600 to-primary-900 flex flex-col">
      <header className="bg-white/10 backdrop-blur-sm">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <button
              onClick={() => navigate('/dashboard')}
              className="flex items-center gap-2 text-white/80 hover:text-white transition-colors"
            >
              <Home className="w-5 h-5" />
              <span className="hidden sm:inline">Dashboard</span>
            </button>
            <div className="text-white text-center">
              <p className="text-sm opacity-80">Domanda</p>
              <p className="text-xl font-bold">{currentIndex + 1} / {questions.length}</p>
            </div>
            <div className="w-20" />
          </div>
        </div>
        <div className="h-1 bg-white/20">
          <div 
            className="h-full bg-white transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
      </header>

      <main className="flex-1 flex items-center justify-center p-4">
        <div className="w-full max-w-3xl animate-fade-in">
          <div className="bg-white rounded-2xl shadow-2xl overflow-hidden">
            <div className="bg-primary-50 px-6 py-4 border-b border-primary-100">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-primary-600 font-semibold">{currentQuestion.category}</p>
                  {currentQuestion.subcategory && (
                    <p className="text-primary-400 text-sm">{currentQuestion.subcategory}</p>
                  )}
                </div>
                <div className="text-right">
                  <p className="text-sm text-primary-500">
                    {categoryProgress.answered}/{categoryProgress.total} in questa categoria
                  </p>
                </div>
              </div>
            </div>

            <div className="p-6 sm:p-8">
              <h2 className="text-xl sm:text-2xl font-semibold text-gray-800 mb-8">
                {currentQuestion.text}
              </h2>

              <div className="space-y-3">
                {currentQuestion.options.map((option, index) => (
                  <button
                    key={index}
                    onClick={() => handleSelectOption(index)}
                    className={`w-full text-left p-4 rounded-xl border-2 transition-all ${
                      currentAnswer?.selected_option === index
                        ? 'border-primary-500 bg-primary-50 text-primary-700'
                        : 'border-gray-200 hover:border-primary-200 hover:bg-gray-50'
                    }`}
                  >
                    <div className="flex items-center gap-4">
                      <div className={`w-6 h-6 rounded-full border-2 flex items-center justify-center flex-shrink-0 ${
                        currentAnswer?.selected_option === index
                          ? 'border-primary-500 bg-primary-500'
                          : 'border-gray-300'
                      }`}>
                        {currentAnswer?.selected_option === index && (
                          <Check className="w-4 h-4 text-white" />
                        )}
                      </div>
                      <span className="text-base">{option.text}</span>
                    </div>
                  </button>
                ))}
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
                  disabled={!allAnswered || submitting}
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
                  disabled={!currentAnswer}
                  className="flex items-center gap-2 px-8 py-3 bg-primary-600 text-white rounded-xl font-semibold hover:bg-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  Successiva
                  <ChevronRight className="w-5 h-5" />
                </button>
              )}
            </div>
          </div>

          <div className="mt-6 flex justify-center gap-1 flex-wrap">
            {questions.map((_, index) => (
              <button
                key={index}
                onClick={() => setCurrentIndex(index)}
                className={`w-3 h-3 rounded-full transition-all ${
                  index === currentIndex
                    ? 'bg-white scale-125'
                    : answers.has(questions[index].id)
                    ? 'bg-white/60'
                    : 'bg-white/30'
                }`}
              />
            ))}
          </div>
        </div>
      </main>
    </div>
  );
};

export default AssessmentPage;
