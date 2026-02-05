import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Shield, 
  Building2, 
  FileText, 
  Eye,
  Download,
  ArrowLeft,
  Users,
  CheckCircle,
  Clock,
  BarChart3,
  Key,
  X,
  Loader2,
  Trash2
} from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';

const API_BASE = import.meta.env.VITE_API_URL || '/api';

interface Assessment {
  id: number;
  status: string;
  maturity_level: number | null;
  created_at: string | null;
  completed_at: string | null;
}

interface Organization {
  id: number;
  name: string;
  type: string;
  sector: string | null;
  size: string | null;
  email: string | null;
  access_code: string;
  created_at: string | null;
  assessments_count: number;
  assessments: Assessment[];
}

interface Stats {
  total_organizations: number;
  total_assessments: number;
  completed_assessments: number;
  in_progress_assessments: number;
  average_maturity_level: number;
}

interface AssessmentDetail {
  id: number;
  organization: {
    id: number;
    name: string;
    type: string;
    sector: string | null;
    size: string | null;
  } | null;
  status: string;
  maturity_level: number | null;
  scores: Record<string, number>;
  gap_analysis: Record<string, any>;
  report: string;
  created_at: string | null;
  completed_at: string | null;
}

const AdminPage: React.FC = () => {
  const navigate = useNavigate();
  const [adminKey, setAdminKey] = useState('');
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [selectedAssessment, setSelectedAssessment] = useState<AssessmentDetail | null>(null);
  const [viewMode, setViewMode] = useState<'list' | 'detail'>('list');
  const [resetPasswordModal, setResetPasswordModal] = useState<{open: boolean; orgId: number; orgName: string} | null>(null);
  const [newPassword, setNewPassword] = useState('');
  const [resetSuccess, setResetSuccess] = useState('');
  const [generatingPdf, setGeneratingPdf] = useState(false);
  const reportRef = useRef<HTMLDivElement>(null);

  const handleLogin = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await fetch(`${API_BASE}/admin/organizations?admin_key=${adminKey}`);
      if (!response.ok) {
        throw new Error('Chiave admin non valida');
      }
      const data = await response.json();
      setOrganizations(data.organizations);
      setIsAuthenticated(true);
      
      const statsResponse = await fetch(`${API_BASE}/admin/stats?admin_key=${adminKey}`);
      if (statsResponse.ok) {
        const statsData = await statsResponse.json();
        setStats(statsData);
      }
    } catch (err: any) {
      setError(err.message || 'Errore di autenticazione');
    } finally {
      setLoading(false);
    }
  };

  const handleResetPassword = async () => {
    if (!resetPasswordModal || !newPassword) return;
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/admin/reset-password`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          organization_id: resetPasswordModal.orgId,
          new_password: newPassword,
          admin_key: adminKey
        })
      });
      if (response.ok) {
        const data = await response.json();
        setResetSuccess(`Password resettata! Codice accesso: ${data.access_code}`);
        setNewPassword('');
        setTimeout(() => {
          setResetPasswordModal(null);
          setResetSuccess('');
        }, 3000);
      } else {
        setError('Errore nel reset della password');
      }
    } catch (err) {
      setError('Errore di connessione');
    } finally {
      setLoading(false);
    }
  };

  const viewAssessmentDetail = async (assessmentId: number) => {
    setLoading(true);
    try {
      const response = await fetch(`${API_BASE}/admin/assessments/${assessmentId}?admin_key=${adminKey}`);
      if (response.ok) {
        const data = await response.json();
        setSelectedAssessment(data);
        setViewMode('detail');
      }
    } catch (err) {
      console.error('Error loading assessment:', err);
    } finally {
      setLoading(false);
    }
  };

  const deleteAssessment = async (assessmentId: number) => {
    if (!confirm('Sei sicuro di voler eliminare questo assessment?')) return;
    
    try {
      const response = await fetch(`${API_BASE}/admin/assessments/${assessmentId}?admin_key=${adminKey}`, {
        method: 'DELETE'
      });
      if (response.ok) {
        handleLogin();
      }
    } catch (err) {
      console.error('Error deleting assessment:', err);
    }
  };

  const deleteOrganization = async (orgId: number, orgName: string) => {
    if (!confirm(`Sei sicuro di voler eliminare "${orgName}" e tutti i suoi assessment?`)) return;
    
    try {
      const response = await fetch(`${API_BASE}/admin/organizations/${orgId}?admin_key=${adminKey}`, {
        method: 'DELETE'
      });
      if (response.ok) {
        handleLogin();
      }
    } catch (err) {
      console.error('Error deleting organization:', err);
    }
  };

  const downloadReport = () => {
    if (!selectedAssessment?.report) return;
    const blob = new Blob([selectedAssessment.report], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `report-${selectedAssessment.organization?.name || 'assessment'}-${selectedAssessment.id}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const downloadPdf = async () => {
    if (!reportRef.current || !selectedAssessment) return;
    
    setGeneratingPdf(true);
    try {
      const canvas = await html2canvas(reportRef.current, {
        useCORS: true,
        logging: false,
        backgroundColor: '#f9fafb'
      } as any);
      
      const imgData = canvas.toDataURL('image/png');
      const pdf = new jsPDF({
        orientation: 'portrait',
        unit: 'mm',
        format: 'a4'
      });
      
      const pdfWidth = pdf.internal.pageSize.getWidth();
      const pdfHeight = pdf.internal.pageSize.getHeight();
      const imgWidth = canvas.width;
      const imgHeight = canvas.height;
      const ratio = Math.min(pdfWidth / imgWidth, pdfHeight / imgHeight);
      const imgX = (pdfWidth - imgWidth * ratio) / 2;
      
      let heightLeft = imgHeight * ratio;
      let position = 0;
      
      pdf.addImage(imgData, 'PNG', imgX, position, imgWidth * ratio, imgHeight * ratio);
      heightLeft -= pdfHeight;
      
      while (heightLeft > 0) {
        position = heightLeft - imgHeight * ratio;
        pdf.addPage();
        pdf.addImage(imgData, 'PNG', imgX, position, imgWidth * ratio, imgHeight * ratio);
        heightLeft -= pdfHeight;
      }
      
      pdf.save(`report-${selectedAssessment.organization?.name || 'assessment'}-${selectedAssessment.id}.pdf`);
    } catch (error) {
      console.error('Error generating PDF:', error);
    } finally {
      setGeneratingPdf(false);
    }
  };

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-800 to-gray-900 flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full">
          <div className="text-center mb-8">
            <div className="w-20 h-20 bg-yellow-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <Shield className="w-10 h-10 text-yellow-600" />
            </div>
            <h1 className="text-2xl font-bold text-gray-800">Pannello Amministratore</h1>
            <p className="text-gray-500 mt-2">Inserisci la chiave admin per accedere</p>
          </div>

          {error && (
            <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-sm">
              {error}
            </div>
          )}

          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Chiave Admin
              </label>
              <input
                type="password"
                value={adminKey}
                onChange={(e) => setAdminKey(e.target.value)}
                onKeyPress={(e) => e.key === 'Enter' && handleLogin()}
                className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-yellow-500 focus:border-transparent"
                placeholder="Inserisci la chiave segreta"
              />
            </div>
            <button
              onClick={handleLogin}
              disabled={loading || !adminKey}
              className="w-full bg-yellow-500 text-white py-4 rounded-xl font-semibold hover:bg-yellow-600 transition-colors disabled:opacity-50"
            >
              {loading ? 'Verifica...' : 'Accedi'}
            </button>
          </div>

          <button
            onClick={() => navigate('/')}
            className="mt-6 w-full text-gray-500 hover:text-gray-700 text-sm"
          >
            ← Torna al login utente
          </button>
        </div>
      </div>
    );
  }

  if (viewMode === 'detail' && selectedAssessment) {
    return (
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow-sm sticky top-0 z-10">
          <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <button
                  onClick={() => setViewMode('list')}
                  className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg"
                >
                  <ArrowLeft className="w-5 h-5" />
                </button>
                <div>
                  <h1 className="text-xl font-bold text-gray-800">
                    Report - {selectedAssessment.organization?.name}
                  </h1>
                  <p className="text-sm text-gray-500">
                    Assessment #{selectedAssessment.id}
                  </p>
                </div>
              </div>
              <div className="flex items-center gap-2">
                <button
                  onClick={downloadPdf}
                  disabled={generatingPdf}
                  className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
                >
                  {generatingPdf ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    <FileText className="w-5 h-5" />
                  )}
                  {generatingPdf ? 'Generazione...' : 'Scarica PDF'}
                </button>
                <button
                  onClick={downloadReport}
                  className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
                >
                  <Download className="w-5 h-5" />
                  Scarica MD
                </button>
              </div>
            </div>
          </div>
        </header>

        <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8" ref={reportRef}>
          <div className="grid md:grid-cols-3 gap-6 mb-8">
            <div className="bg-white rounded-xl shadow-sm p-6">
              <p className="text-sm text-gray-500 mb-1">Organizzazione</p>
              <p className="text-xl font-bold text-gray-800">{selectedAssessment.organization?.name}</p>
              <p className="text-sm text-gray-500 mt-1">
                {selectedAssessment.organization?.type} - {selectedAssessment.organization?.sector}
              </p>
            </div>
            <div className="bg-white rounded-xl shadow-sm p-6">
              <p className="text-sm text-gray-500 mb-1">Livello Maturità</p>
              <p className="text-4xl font-bold text-primary-600">
                {selectedAssessment.maturity_level?.toFixed(1) || 'N/A'}
                <span className="text-lg text-gray-400"> / 5</span>
              </p>
            </div>
            <div className="bg-white rounded-xl shadow-sm p-6">
              <p className="text-sm text-gray-500 mb-1">Data Completamento</p>
              <p className="text-xl font-bold text-gray-800">
                {selectedAssessment.completed_at 
                  ? new Date(selectedAssessment.completed_at).toLocaleDateString('it-IT')
                  : 'Non completato'}
              </p>
            </div>
          </div>

          {selectedAssessment.scores && Object.keys(selectedAssessment.scores).length > 0 && (
            <div className="bg-white rounded-xl shadow-sm p-6 mb-8">
              <h2 className="text-lg font-semibold text-gray-800 mb-4">Punteggi per Area</h2>
              <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
                {Object.entries(selectedAssessment.scores).map(([category, score]) => (
                  <div key={category} className="p-4 bg-gray-50 rounded-lg">
                    <p className="text-sm text-gray-600 mb-1">{category}</p>
                    <div className="flex items-end gap-2">
                      <span className="text-2xl font-bold text-primary-600">{score.toFixed(1)}</span>
                      <span className="text-gray-400 mb-1">/ 5</span>
                    </div>
                    <div className="w-full bg-gray-200 rounded-full h-2 mt-2">
                      <div 
                        className="bg-primary-500 h-2 rounded-full"
                        style={{ width: `${(score / 5) * 100}%` }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {selectedAssessment.report && (
            <div className="bg-white rounded-xl shadow-sm p-6">
              <h2 className="text-lg font-semibold text-gray-800 mb-4">Report Completo</h2>
              <div className="prose max-w-none">
                <ReactMarkdown>{selectedAssessment.report}</ReactMarkdown>
              </div>
            </div>
          )}
        </main>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <Shield className="w-8 h-8 text-yellow-500" />
              <div>
                <h1 className="text-xl font-bold text-gray-800">Pannello Admin</h1>
                <p className="text-sm text-gray-500">Gestione Assessment</p>
              </div>
            </div>
            <button
              onClick={() => {
                setIsAuthenticated(false);
                setAdminKey('');
              }}
              className="text-gray-500 hover:text-gray-700"
            >
              Esci
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
        {stats && (
          <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-8">
            <div className="bg-white rounded-xl shadow-sm p-4">
              <div className="flex items-center gap-3">
                <Users className="w-8 h-8 text-blue-500" />
                <div>
                  <p className="text-2xl font-bold text-gray-800">{stats.total_organizations}</p>
                  <p className="text-xs text-gray-500">Organizzazioni</p>
                </div>
              </div>
            </div>
            <div className="bg-white rounded-xl shadow-sm p-4">
              <div className="flex items-center gap-3">
                <FileText className="w-8 h-8 text-purple-500" />
                <div>
                  <p className="text-2xl font-bold text-gray-800">{stats.total_assessments}</p>
                  <p className="text-xs text-gray-500">Assessment Totali</p>
                </div>
              </div>
            </div>
            <div className="bg-white rounded-xl shadow-sm p-4">
              <div className="flex items-center gap-3">
                <CheckCircle className="w-8 h-8 text-green-500" />
                <div>
                  <p className="text-2xl font-bold text-gray-800">{stats.completed_assessments}</p>
                  <p className="text-xs text-gray-500">Completati</p>
                </div>
              </div>
            </div>
            <div className="bg-white rounded-xl shadow-sm p-4">
              <div className="flex items-center gap-3">
                <Clock className="w-8 h-8 text-orange-500" />
                <div>
                  <p className="text-2xl font-bold text-gray-800">{stats.in_progress_assessments}</p>
                  <p className="text-xs text-gray-500">In Corso</p>
                </div>
              </div>
            </div>
            <div className="bg-white rounded-xl shadow-sm p-4">
              <div className="flex items-center gap-3">
                <BarChart3 className="w-8 h-8 text-primary-500" />
                <div>
                  <p className="text-2xl font-bold text-gray-800">{stats.average_maturity_level}</p>
                  <p className="text-xs text-gray-500">Media Maturità</p>
                </div>
              </div>
            </div>
          </div>
        )}

        <div className="bg-white rounded-xl shadow-sm overflow-hidden">
          <div className="px-6 py-4 border-b border-gray-100">
            <h2 className="text-lg font-semibold text-gray-800">Organizzazioni Registrate</h2>
          </div>
          
          {organizations.length === 0 ? (
            <div className="p-8 text-center text-gray-500">
              Nessuna organizzazione registrata
            </div>
          ) : (
            <div className="divide-y divide-gray-100">
              {organizations.map((org) => (
                <div key={org.id} className="p-6">
                  <div className="flex items-start justify-between mb-4">
                    <div className="flex items-center gap-4">
                      <div className="w-12 h-12 bg-primary-100 rounded-full flex items-center justify-center">
                        <Building2 className="w-6 h-6 text-primary-600" />
                      </div>
                      <div>
                        <h3 className="font-semibold text-gray-800">{org.name}</h3>
                        <p className="text-sm text-gray-500">
                          {org.type} {org.sector && `• ${org.sector}`} {org.size && `• ${org.size}`}
                        </p>
                        <p className="text-xs text-gray-400 mt-1">
                          Codice: <span className="font-mono bg-gray-100 px-2 py-0.5 rounded">{org.access_code}</span>
                          {org.email && ` • ${org.email}`}
                        </p>
                      </div>
                    </div>
                    <div className="text-right flex flex-col items-end gap-2">
                      <p className="text-sm text-gray-500">
                        Registrato: {org.created_at ? new Date(org.created_at).toLocaleDateString('it-IT') : 'N/A'}
                      </p>
                      <p className="text-sm font-medium text-primary-600">
                        {org.assessments_count} assessment
                      </p>
                      <div className="flex gap-2">
                        <button
                          onClick={() => setResetPasswordModal({open: true, orgId: org.id, orgName: org.name})}
                          className="flex items-center gap-1 text-xs text-orange-600 hover:text-orange-700 hover:bg-orange-50 px-2 py-1 rounded"
                        >
                          <Key className="w-3 h-3" />
                          Reset Password
                        </button>
                        <button
                          onClick={() => deleteOrganization(org.id, org.name)}
                          className="flex items-center gap-1 text-xs text-red-600 hover:text-red-700 hover:bg-red-50 px-2 py-1 rounded"
                        >
                          <Trash2 className="w-3 h-3" />
                          Elimina
                        </button>
                      </div>
                    </div>
                  </div>

                  {org.assessments.length > 0 && (
                    <div className="ml-16 space-y-2">
                      {org.assessments.map((assessment) => (
                        <div 
                          key={assessment.id}
                          className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                        >
                          <div className="flex items-center gap-3">
                            <FileText className="w-5 h-5 text-gray-400" />
                            <div>
                              <p className="text-sm font-medium text-gray-700">
                                Assessment #{assessment.id}
                              </p>
                              <p className="text-xs text-gray-500">
                                {assessment.created_at 
                                  ? new Date(assessment.created_at).toLocaleDateString('it-IT')
                                  : 'N/A'}
                              </p>
                            </div>
                          </div>
                          <div className="flex items-center gap-4">
                            <span className={`px-2 py-1 rounded-full text-xs font-medium ${
                              assessment.status === 'completed' 
                                ? 'bg-green-100 text-green-700'
                                : 'bg-yellow-100 text-yellow-700'
                            }`}>
                              {assessment.status === 'completed' ? 'Completato' : 'In corso'}
                            </span>
                            {assessment.maturity_level && (
                              <span className="text-sm font-semibold text-primary-600">
                                {assessment.maturity_level.toFixed(1)}/5
                              </span>
                            )}
                            {assessment.status === 'completed' && (
                              <button
                                onClick={() => viewAssessmentDetail(assessment.id)}
                                className="p-2 text-gray-400 hover:text-primary-600 hover:bg-primary-50 rounded-lg"
                              >
                                <Eye className="w-5 h-5" />
                              </button>
                            )}
                            <button
                              onClick={() => deleteAssessment(assessment.id)}
                              className="p-2 text-gray-400 hover:text-red-600 hover:bg-red-50 rounded-lg"
                            >
                              <Trash2 className="w-5 h-5" />
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      </main>

      {/* Password Reset Modal */}
      {resetPasswordModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white rounded-xl shadow-2xl p-6 max-w-md w-full mx-4">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-800">Reset Password</h3>
              <button
                onClick={() => {
                  setResetPasswordModal(null);
                  setNewPassword('');
                  setResetSuccess('');
                }}
                className="p-1 text-gray-400 hover:text-gray-600"
              >
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <p className="text-sm text-gray-600 mb-4">
              Stai resettando la password per: <strong>{resetPasswordModal.orgName}</strong>
            </p>

            {resetSuccess ? (
              <div className="p-4 bg-green-50 border border-green-200 rounded-lg text-green-700 text-sm">
                {resetSuccess}
              </div>
            ) : (
              <>
                <div className="mb-4">
                  <label className="block text-sm font-medium text-gray-700 mb-2">
                    Nuova Password
                  </label>
                  <input
                    type="text"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    className="w-full px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Inserisci nuova password"
                  />
                </div>
                <div className="flex gap-3">
                  <button
                    onClick={() => {
                      setResetPasswordModal(null);
                      setNewPassword('');
                    }}
                    className="flex-1 px-4 py-3 border border-gray-300 text-gray-700 rounded-xl hover:bg-gray-50"
                  >
                    Annulla
                  </button>
                  <button
                    onClick={handleResetPassword}
                    disabled={loading || !newPassword}
                    className="flex-1 px-4 py-3 bg-orange-500 text-white rounded-xl hover:bg-orange-600 disabled:opacity-50"
                  >
                    {loading ? 'Resettando...' : 'Reset Password'}
                  </button>
                </div>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminPage;
