import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { 
  ChevronLeft, 
  ChevronRight, 
  Check, 
  Loader2,
  Home,
  HelpCircle,
  X,
  MessageCircle,
  Send
} from 'lucide-react';
import { questionsApi, assessmentsApi, assistantApi, organizationApi } from '../api';
import { Question, Answer } from '../types';
import { useAuth } from '../context/AuthContext';

const AssessmentPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { organization, updateOrganization } = useAuth();
  const [questions, setQuestions] = useState<Question[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Map<number, Answer>>(new Map());
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [_categories, setCategories] = useState<string[]>([]);
  const [showHint, setShowHint] = useState(false);
  const [showChat, setShowChat] = useState(false);
  const [chatMessage, setChatMessage] = useState('');
  const [chatResponse, setChatResponse] = useState('');
  const [chatLoading, setChatLoading] = useState(false);
  const [showMissingDataModal, setShowMissingDataModal] = useState(false);
  const [missingData, setMissingData] = useState({
    fiscal_code: '',
    phone: '',
    admin_name: '',
    sector: '',
    size: ''
  });

  useEffect(() => {
    loadQuestions();
  }, []);

  useEffect(() => {
    setShowHint(false);
    setShowChat(false);
    setChatMessage('');
    setChatResponse('');
  }, [currentIndex]);

  const handleSendChat = async () => {
    if (!chatMessage.trim() || !currentQuestion) return;
    
    setChatLoading(true);
    try {
      const response = await assistantApi.chat({
        question_text: currentQuestion.text,
        question_hint: currentQuestion.hint || '',
        options: currentQuestion.options.map(o => o.text),
        user_message: chatMessage,
        organization_type: organization?.type || 'azienda',
        organization_sector: organization?.sector || '',
      });
      setChatResponse(response.response);
    } catch (error) {
      setChatResponse('Errore nella comunicazione con l\'assistente. Riprova più tardi.');
    } finally {
      setChatLoading(false);
    }
  };

  const loadQuestions = async () => {
    try {
      const data = await questionsApi.getQuestions();
      setQuestions(data);
      const uniqueCategories = [...new Set(data.map(q => q.category))];
      setCategories(uniqueCategories);
      
      // Load saved progress if exists
      if (id) {
        try {
          const assessment = await assessmentsApi.getById(parseInt(id));
          if (assessment.responses?.answers && assessment.status === 'in_progress') {
            const savedAnswers = new Map<number, Answer>();
            for (const ans of assessment.responses.answers) {
              savedAnswers.set(ans.question_id, {
                question_id: ans.question_id,
                selected_option: ans.selected_option,
                notes: ans.notes || ''
              });
            }
            setAnswers(savedAnswers);
            // Go to first unanswered question
            const firstUnanswered = data.findIndex(q => !savedAnswers.has(q.id));
            if (firstUnanswered > 0) {
              setCurrentIndex(firstUnanswered);
            } else if (savedAnswers.size === data.length) {
              setCurrentIndex(data.length - 1);
            }
          }
        } catch (e) {
          console.log('No saved progress found');
        }
      }
    } catch (error) {
      console.error('Error loading questions:', error);
    } finally {
      setLoading(false);
    }
  };

  const currentQuestion = questions[currentIndex];
  const progress = ((currentIndex + 1) / questions.length) * 100;

  const handleSelectOption = async (optionIndex: number) => {
    const newAnswers = new Map(answers);
    newAnswers.set(currentQuestion.id, {
      question_id: currentQuestion.id,
      selected_option: optionIndex
    });
    setAnswers(newAnswers);
    
    // Auto-save progress
    if (id) {
      try {
        const answersArray = Array.from(newAnswers.values());
        await assessmentsApi.saveProgress(parseInt(id), answersArray);
      } catch (error) {
        console.error('Error auto-saving:', error);
      }
    }
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

  const checkMissingData = () => {
    if (!organization) return false;
    return !organization.fiscal_code || !organization.phone || !organization.admin_name || 
           !organization.sector || !organization.size;
  };

  const handleSubmit = async () => {
    if (!id) return;
    
    if (checkMissingData()) {
      setMissingData({
        fiscal_code: organization?.fiscal_code || '',
        phone: organization?.phone || '',
        admin_name: organization?.admin_name || '',
        sector: organization?.sector || '',
        size: organization?.size || ''
      });
      setShowMissingDataModal(true);
      return;
    }
    
    await submitAssessment();
  };

  const submitAssessment = async () => {
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

  const handleSaveMissingData = async () => {
    setSubmitting(true);
    try {
      const updatedOrg = await organizationApi.update(missingData);
      updateOrganization(updatedOrg);
      setShowMissingDataModal(false);
      await submitAssessment();
    } catch (error) {
      console.error('Error updating organization:', error);
      alert('Errore nel salvataggio dei dati. Riprova.');
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
              <div className="flex items-start justify-between gap-4 mb-8">
                <h2 className="text-xl sm:text-2xl font-semibold text-gray-800">
                  {currentQuestion.text}
                </h2>
                <div className="flex gap-2 flex-shrink-0">
                  {currentQuestion.hint && (
                    <button
                      onClick={() => setShowHint(!showHint)}
                      className={`p-2 rounded-full transition-colors ${
                        showHint ? 'bg-primary-100 text-primary-600' : 'text-gray-400 hover:text-primary-500 hover:bg-gray-100'
                      }`}
                      title="Mostra suggerimento"
                    >
                      <HelpCircle className="w-6 h-6" />
                    </button>
                  )}
                  <button
                    onClick={() => setShowChat(!showChat)}
                    className={`p-2 rounded-full transition-colors ${
                      showChat ? 'bg-green-100 text-green-600' : 'text-gray-400 hover:text-green-500 hover:bg-gray-100'
                    }`}
                    title="Chiedi all'assistente AI"
                  >
                    <MessageCircle className="w-6 h-6" />
                  </button>
                </div>
              </div>

              {showHint && currentQuestion.hint && (
                <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-xl relative">
                  <button
                    onClick={() => setShowHint(false)}
                    className="absolute top-2 right-2 p-1 text-blue-400 hover:text-blue-600"
                  >
                    <X className="w-4 h-4" />
                  </button>
                  <p className="text-sm text-blue-800 pr-6">
                    <strong>💡 Suggerimento:</strong> {currentQuestion.hint}
                  </p>
                </div>
              )}

              {showChat && (
                <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-xl">
                  <div className="flex items-center justify-between mb-3">
                    <h3 className="font-semibold text-green-800 flex items-center gap-2">
                      <MessageCircle className="w-5 h-5" />
                      Assistente AI
                    </h3>
                    <button
                      onClick={() => setShowChat(false)}
                      className="p-1 text-green-400 hover:text-green-600"
                    >
                      <X className="w-4 h-4" />
                    </button>
                  </div>
                  
                  {chatResponse && (
                    <div className="mb-4 p-3 bg-white rounded-lg border border-green-100">
                      <p className="text-sm text-gray-700 whitespace-pre-wrap">{chatResponse}</p>
                    </div>
                  )}
                  
                  <div className="flex gap-2">
                    <input
                      type="text"
                      value={chatMessage}
                      onChange={(e) => setChatMessage(e.target.value)}
                      onKeyDown={(e) => e.key === 'Enter' && handleSendChat()}
                      placeholder="Chiedi aiuto su questa domanda..."
                      className="flex-1 px-4 py-2 border border-green-200 rounded-lg text-sm focus:ring-2 focus:ring-green-500 focus:border-transparent"
                      disabled={chatLoading}
                    />
                    <button
                      onClick={handleSendChat}
                      disabled={chatLoading || !chatMessage.trim()}
                      className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {chatLoading ? (
                        <Loader2 className="w-5 h-5 animate-spin" />
                      ) : (
                        <Send className="w-5 h-5" />
                      )}
                    </button>
                  </div>
                </div>
              )}

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

      {showMissingDataModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-white rounded-2xl shadow-2xl max-w-lg w-full max-h-[90vh] overflow-y-auto">
            <div className="p-6 border-b border-gray-100">
              <h2 className="text-xl font-bold text-gray-800">Completa i tuoi dati</h2>
              <p className="text-sm text-gray-500 mt-1">
                Prima di completare l'assessment, inserisci i dati mancanti per generare un report completo.
              </p>
            </div>
            
            <div className="p-6 space-y-4">
              {!organization?.admin_name && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Nome Responsabile *
                  </label>
                  <input
                    type="text"
                    value={missingData.admin_name}
                    onChange={(e) => setMissingData({...missingData, admin_name: e.target.value})}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    placeholder="Nome e cognome del responsabile"
                  />
                </div>
              )}
              
              {!organization?.fiscal_code && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Codice Fiscale / P.IVA *
                  </label>
                  <input
                    type="text"
                    value={missingData.fiscal_code}
                    onChange={(e) => setMissingData({...missingData, fiscal_code: e.target.value})}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    placeholder="Codice fiscale o partita IVA"
                  />
                </div>
              )}
              
              {!organization?.phone && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Telefono *
                  </label>
                  <input
                    type="tel"
                    value={missingData.phone}
                    onChange={(e) => setMissingData({...missingData, phone: e.target.value})}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                    placeholder="+39 xxx xxx xxxx"
                  />
                </div>
              )}
              
              {!organization?.sector && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Settore *
                  </label>
                  <select
                    value={missingData.sector}
                    onChange={(e) => setMissingData({...missingData, sector: e.target.value})}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    <option value="">Seleziona settore</option>
                    <option value="manifatturiero">Manifatturiero</option>
                    <option value="servizi">Servizi</option>
                    <option value="commercio">Commercio</option>
                    <option value="tecnologia">Tecnologia</option>
                    <option value="sanita">Sanità</option>
                    <option value="istruzione">Istruzione</option>
                    <option value="finanza">Finanza</option>
                    <option value="pubblica_amministrazione">Pubblica Amministrazione</option>
                    <option value="altro">Altro</option>
                  </select>
                </div>
              )}
              
              {!organization?.size && (
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Dimensione Organizzazione *
                  </label>
                  <select
                    value={missingData.size}
                    onChange={(e) => setMissingData({...missingData, size: e.target.value})}
                    className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  >
                    <option value="">Seleziona dimensione</option>
                    <option value="1-10">1-10 dipendenti</option>
                    <option value="11-50">11-50 dipendenti</option>
                    <option value="51-250">51-250 dipendenti</option>
                    <option value="251-1000">251-1000 dipendenti</option>
                    <option value="1000+">Oltre 1000 dipendenti</option>
                  </select>
                </div>
              )}
            </div>
            
            <div className="p-6 border-t border-gray-100 flex gap-3">
              <button
                onClick={() => setShowMissingDataModal(false)}
                className="flex-1 px-4 py-3 border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
              >
                Annulla
              </button>
              <button
                onClick={handleSaveMissingData}
                disabled={submitting}
                className="flex-1 px-4 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50 transition-colors flex items-center justify-center gap-2"
              >
                {submitting ? (
                  <>
                    <Loader2 className="w-5 h-5 animate-spin" />
                    Salvataggio...
                  </>
                ) : (
                  <>
                    <Check className="w-5 h-5" />
                    Salva e Completa
                  </>
                )}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AssessmentPage;
