import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  BarChart3, 
  ClipboardList, 
  LogOut, 
  Plus, 
  FileText,
  Building2,
  Clock,
  CheckCircle2
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { assessmentsApi } from '../api';
import { Assessment } from '../types';

const Dashboard: React.FC = () => {
  const { organization, logout } = useAuth();
  const navigate = useNavigate();
  const [assessments, setAssessments] = useState<Assessment[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAssessments();
  }, []);

  const loadAssessments = async () => {
    try {
      const data = await assessmentsApi.getAll();
      setAssessments(data);
    } catch (error) {
      console.error('Error loading assessments:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleNewAssessment = async () => {
    try {
      const assessment = await assessmentsApi.create();
      navigate(`/assessment/${assessment.id}`);
    } catch (error) {
      console.error('Error creating assessment:', error);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('it-IT', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'completed':
        return (
          <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm font-medium bg-green-100 text-green-700">
            <CheckCircle2 className="w-4 h-4" />
            Completato
          </span>
        );
      case 'in_progress':
        return (
          <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm font-medium bg-yellow-100 text-yellow-700">
            <Clock className="w-4 h-4" />
            In corso
          </span>
        );
      default:
        return (
          <span className="inline-flex items-center gap-1 px-3 py-1 rounded-full text-sm font-medium bg-gray-100 text-gray-700">
            {status}
          </span>
        );
    }
  };

  const getMaturityLabel = (level: number | null) => {
    if (level === null) return '-';
    if (level < 2) return 'Iniziale';
    if (level < 3) return 'Gestito';
    if (level < 4) return 'Definito';
    if (level < 5) return 'Avanzato';
    return 'Ottimizzato';
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <div className="w-12 h-12 bg-primary-100 rounded-xl flex items-center justify-center">
                <Building2 className="w-6 h-6 text-primary-600" />
              </div>
              <div>
                <h1 className="text-xl font-bold text-gray-800">{organization?.name}</h1>
                <p className="text-sm text-gray-500">
                  Codice: <span className="font-mono">{organization?.access_code}</span>
                </p>
              </div>
            </div>
            <button
              onClick={handleLogout}
              className="flex items-center gap-2 px-4 py-2 text-gray-600 hover:text-gray-800 hover:bg-gray-100 rounded-lg transition-colors"
            >
              <LogOut className="w-5 h-5" />
              <span className="hidden sm:inline">Esci</span>
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
          <div>
            <h2 className="text-2xl font-bold text-gray-800">I tuoi Assessment</h2>
            <p className="text-gray-500 mt-1">Gestisci le valutazioni di maturità digitale</p>
          </div>
          <button
            onClick={handleNewAssessment}
            className="inline-flex items-center gap-2 px-6 py-3 bg-primary-600 text-white rounded-xl font-semibold hover:bg-primary-700 transition-colors shadow-lg shadow-primary-200"
          >
            <Plus className="w-5 h-5" />
            Nuovo Assessment
          </button>
        </div>

        {loading ? (
          <div className="flex items-center justify-center py-20">
            <div className="w-12 h-12 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin" />
          </div>
        ) : assessments.length === 0 ? (
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-12 text-center">
            <div className="w-20 h-20 bg-primary-50 rounded-full flex items-center justify-center mx-auto mb-6">
              <ClipboardList className="w-10 h-10 text-primary-400" />
            </div>
            <h3 className="text-xl font-semibold text-gray-800 mb-2">Nessun assessment</h3>
            <p className="text-gray-500 mb-6">Inizia la tua prima valutazione di maturità digitale</p>
            <button
              onClick={handleNewAssessment}
              className="inline-flex items-center gap-2 px-6 py-3 bg-primary-600 text-white rounded-xl font-semibold hover:bg-primary-700 transition-colors"
            >
              <Plus className="w-5 h-5" />
              Inizia Assessment
            </button>
          </div>
        ) : (
          <div className="grid gap-4">
            {assessments.map((assessment) => (
              <div
                key={assessment.id}
                className="bg-white rounded-xl shadow-sm border border-gray-100 p-6 hover:shadow-md transition-shadow cursor-pointer"
                onClick={() => {
                  if (assessment.status === 'completed') {
                    navigate(`/report/${assessment.id}`);
                  } else {
                    navigate(`/assessment/${assessment.id}`);
                  }
                }}
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                  <div className="flex items-center gap-4">
                    <div className="w-12 h-12 bg-gray-100 rounded-xl flex items-center justify-center">
                      {assessment.status === 'completed' ? (
                        <BarChart3 className="w-6 h-6 text-primary-600" />
                      ) : (
                        <ClipboardList className="w-6 h-6 text-gray-400" />
                      )}
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-800">
                        Assessment #{assessment.id}
                      </h3>
                      <p className="text-sm text-gray-500">
                        Creato il {formatDate(assessment.created_at)}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-4">
                    {assessment.maturity_level !== null && (
                      <div className="text-right">
                        <p className="text-2xl font-bold text-primary-600">
                          {assessment.maturity_level.toFixed(1)}
                        </p>
                        <p className="text-xs text-gray-500">
                          {getMaturityLabel(assessment.maturity_level)}
                        </p>
                      </div>
                    )}
                    {getStatusBadge(assessment.status)}
                    {assessment.status === 'completed' && (
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          navigate(`/report/${assessment.id}`);
                        }}
                        className="p-2 text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
                      >
                        <FileText className="w-5 h-5" />
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
};

export default Dashboard;
