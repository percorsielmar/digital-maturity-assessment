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
  CheckCircle2,
  Download,
  Edit2,
  Save,
  X
} from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { assessmentsApi, organizationApi } from '../api';
import { Assessment } from '../types';

const Dashboard: React.FC = () => {
  const { organization, logout, updateOrganization } = useAuth();
  const navigate = useNavigate();
  const [assessments, setAssessments] = useState<Assessment[]>([]);
  const [loading, setLoading] = useState(true);
  const [editingProfile, setEditingProfile] = useState(false);
  const [profileData, setProfileData] = useState({
    admin_name: organization?.admin_name || '',
    fiscal_code: organization?.fiscal_code || '',
    phone: organization?.phone || '',
    sector: organization?.sector || '',
    size: organization?.size || ''
  });
  const [savingProfile, setSavingProfile] = useState(false);

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

  const handleNewAssessment = async (level: number = 1) => {
    try {
      console.log('Creating assessment level:', level);
      const assessment = await assessmentsApi.create(level);
      console.log('Created assessment:', assessment);
      if (level === 2) {
        navigate(`/assessment-level2/${assessment.id}`);
      } else {
        navigate(`/assessment/${assessment.id}`);
      }
    } catch (error: any) {
      console.error('Error creating assessment:', error);
      alert(`Errore: ${error?.response?.data?.detail || error.message || 'Errore sconosciuto'}`);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  const handleSaveProfile = async () => {
    setSavingProfile(true);
    try {
      const updatedOrg = await organizationApi.update(profileData);
      updateOrganization(updatedOrg);
      setEditingProfile(false);
    } catch (error) {
      console.error('Error saving profile:', error);
      alert('Errore nel salvataggio. Riprova.');
    } finally {
      setSavingProfile(false);
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleString('it-IT', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      timeZone: 'Europe/Rome'
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
        {/* Profile Section */}
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 mb-8">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold text-gray-800">Dati Organizzazione</h3>
            {!editingProfile ? (
              <button
                onClick={() => setEditingProfile(true)}
                className="flex items-center gap-2 px-3 py-1.5 text-sm text-primary-600 hover:bg-primary-50 rounded-lg"
              >
                <Edit2 className="w-4 h-4" />
                Modifica
              </button>
            ) : (
              <div className="flex gap-2">
                <button
                  onClick={() => setEditingProfile(false)}
                  className="flex items-center gap-1 px-3 py-1.5 text-sm text-gray-600 hover:bg-gray-100 rounded-lg"
                >
                  <X className="w-4 h-4" />
                  Annulla
                </button>
                <button
                  onClick={handleSaveProfile}
                  disabled={savingProfile}
                  className="flex items-center gap-1 px-3 py-1.5 text-sm bg-primary-600 text-white rounded-lg hover:bg-primary-700 disabled:opacity-50"
                >
                  <Save className="w-4 h-4" />
                  {savingProfile ? 'Salvataggio...' : 'Salva'}
                </button>
              </div>
            )}
          </div>
          
          {editingProfile ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Nome Responsabile</label>
                <input
                  type="text"
                  value={profileData.admin_name}
                  onChange={(e) => setProfileData({...profileData, admin_name: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="Nome e cognome"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">C.F. / P.IVA</label>
                <input
                  type="text"
                  value={profileData.fiscal_code}
                  onChange={(e) => setProfileData({...profileData, fiscal_code: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="Codice fiscale o P.IVA"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Telefono</label>
                <input
                  type="tel"
                  value={profileData.phone}
                  onChange={(e) => setProfileData({...profileData, phone: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                  placeholder="+39 xxx xxx xxxx"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Settore</label>
                <select
                  value={profileData.sector}
                  onChange={(e) => setProfileData({...profileData, sector: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
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
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Dimensione</label>
                <select
                  value={profileData.size}
                  onChange={(e) => setProfileData({...profileData, size: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                >
                  <option value="">Seleziona dimensione</option>
                  <option value="1-10">1-10 dipendenti</option>
                  <option value="11-50">11-50 dipendenti</option>
                  <option value="51-250">51-250 dipendenti</option>
                  <option value="251-1000">251-1000 dipendenti</option>
                  <option value="1000+">Oltre 1000 dipendenti</option>
                </select>
              </div>
            </div>
          ) : (
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-5 gap-4 text-sm">
              <div>
                <p className="text-gray-500">Responsabile</p>
                <p className="font-medium text-gray-800">{organization?.admin_name || '-'}</p>
              </div>
              <div>
                <p className="text-gray-500">C.F. / P.IVA</p>
                <p className="font-medium text-gray-800">{organization?.fiscal_code || '-'}</p>
              </div>
              <div>
                <p className="text-gray-500">Telefono</p>
                <p className="font-medium text-gray-800">{organization?.phone || '-'}</p>
              </div>
              <div>
                <p className="text-gray-500">Settore</p>
                <p className="font-medium text-gray-800">{organization?.sector || '-'}</p>
              </div>
              <div>
                <p className="text-gray-500">Dimensione</p>
                <p className="font-medium text-gray-800">{organization?.size || '-'}</p>
              </div>
            </div>
          )}
        </div>

        <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-8">
          <div>
            <h2 className="text-2xl font-bold text-gray-800">I tuoi Assessment</h2>
            <p className="text-gray-500 mt-1">Gestisci le valutazioni di maturità digitale</p>
          </div>
          <div className="flex flex-wrap gap-3">
            <button
              onClick={() => handleNewAssessment(1)}
              className="inline-flex items-center gap-2 px-6 py-3 bg-primary-600 text-white rounded-xl font-semibold hover:bg-primary-700 transition-colors shadow-lg shadow-primary-200"
            >
              <Plus className="w-5 h-5" />
              Assessment Livello 1
            </button>
            <button
              onClick={() => handleNewAssessment(2)}
              className="inline-flex items-center gap-2 px-6 py-3 bg-green-600 text-white rounded-xl font-semibold hover:bg-green-700 transition-colors shadow-lg shadow-green-200"
            >
              <Plus className="w-5 h-5" />
              Assessment Livello 2
            </button>
          </div>
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
              onClick={() => handleNewAssessment(1)}
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
                  } else if (assessment.level === 2) {
                    navigate(`/assessment-level2/${assessment.id}`);
                  } else {
                    navigate(`/assessment/${assessment.id}`);
                  }
                }}
              >
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                  <div className="flex items-center gap-4">
                    <div className={`w-12 h-12 rounded-xl flex items-center justify-center ${assessment.level === 2 ? 'bg-green-100' : 'bg-gray-100'}`}>
                      {assessment.status === 'completed' ? (
                        <BarChart3 className={`w-6 h-6 ${assessment.level === 2 ? 'text-green-600' : 'text-primary-600'}`} />
                      ) : (
                        <ClipboardList className={`w-6 h-6 ${assessment.level === 2 ? 'text-green-400' : 'text-gray-400'}`} />
                      )}
                    </div>
                    <div>
                      <h3 className="font-semibold text-gray-800">
                        {assessment.level === 2 ? 'Assessment 2' : 'Assessment 1'} 
                        <span className="text-gray-400 font-normal ml-1">#{assessment.id}</span>
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
                      <>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            navigate(`/report/${assessment.id}`);
                          }}
                          className="p-2 text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
                          title="Visualizza Report"
                        >
                          <FileText className="w-5 h-5" />
                        </button>
                        <button
                          onClick={(e) => {
                            e.stopPropagation();
                            navigate(`/report/${assessment.id}?download=pdf`);
                          }}
                          className="p-2 text-green-600 hover:bg-green-50 rounded-lg transition-colors"
                          title="Scarica PDF"
                        >
                          <Download className="w-5 h-5" />
                        </button>
                      </>
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
