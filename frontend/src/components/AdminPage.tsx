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
  Trash2,
  Package,
  ListChecks,
  Printer,
  UserCircle,
  Timer
} from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType } from 'docx';
import { saveAs } from 'file-saver';

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
  audit_sheet?: string;
  created_at: string | null;
  completed_at: string | null;
}

interface StaffProfiles {
  digital_transformation_expert: string;
  process_innovation_analyst: string;
}

interface ResponseDetail {
  question_id: number;
  category: string;
  subcategory: string;
  question_text: string;
  selected_option_index: number;
  selected_option_text: string;
  selected_score: number;
  notes: string | null;
  all_options: { text: string; score: number }[];
}

interface ResponsesData {
  assessment_id: number;
  organization: { name: string; type: string };
  status: string;
  maturity_level: number | null;
  completed_at: string | null;
  total_questions: number;
  responses: ResponseDetail[];
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
  const [generatingDoc, setGeneratingDoc] = useState(false);
  const [staffProfiles, setStaffProfiles] = useState<StaffProfiles | null>(null);
  const [regenerating, setRegenerating] = useState(false);
  const [responsesData, setResponsesData] = useState<ResponsesData | null>(null);
  const [showResponses, setShowResponses] = useState(false);
  const [loadingResponses, setLoadingResponses] = useState(false);
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
      const [assessmentResponse, profilesResponse] = await Promise.all([
        fetch(`${API_BASE}/admin/assessments/${assessmentId}?admin_key=${adminKey}`),
        fetch(`${API_BASE}/assessments/staff-profiles`)
      ]);
      
      if (assessmentResponse.ok) {
        const data = await assessmentResponse.json();
        setSelectedAssessment(data);
        setViewMode('detail');
      }
      
      if (profilesResponse.ok) {
        const profilesData = await profilesResponse.json();
        setStaffProfiles(profilesData.profiles);
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

  const downloadAuditSheet = () => {
    if (!selectedAssessment?.audit_sheet) return;
    const blob = new Blob([selectedAssessment.audit_sheet], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `scheda-audit-${selectedAssessment.organization?.name || 'assessment'}-${selectedAssessment.id}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const regenerateReport = async () => {
    if (!selectedAssessment) return;
    
    setRegenerating(true);
    try {
      const response = await fetch(
        `${API_BASE}/admin/assessments/${selectedAssessment.id}/regenerate?admin_key=${adminKey}`,
        { method: 'POST' }
      );
      
      if (response.ok) {
        const data = await response.json();
        alert(`Report rigenerato con successo!\nLivello maturità: ${data.maturity_level}\nScheda Audit: ${data.has_audit_sheet ? 'Sì' : 'No'}`);
        viewAssessmentDetail(selectedAssessment.id);
      } else {
        const errorData = await response.json();
        alert(`Errore: ${errorData.detail || 'Impossibile rigenerare il report'}`);
      }
    } catch (err) {
      console.error('Error regenerating report:', err);
      alert('Errore di connessione durante la rigenerazione');
    } finally {
      setRegenerating(false);
    }
  };

  const viewResponses = async () => {
    if (!selectedAssessment) return;
    setLoadingResponses(true);
    try {
      const response = await fetch(
        `${API_BASE}/admin/assessments/${selectedAssessment.id}/responses?admin_key=${adminKey}`
      );
      if (response.ok) {
        const data = await response.json();
        setResponsesData(data);
        setShowResponses(true);
      } else {
        alert('Errore nel caricamento delle risposte');
      }
    } catch (err) {
      console.error('Error loading responses:', err);
      alert('Errore di connessione');
    } finally {
      setLoadingResponses(false);
    }
  };

  const printResponses = () => {
    const printWindow = window.open('', '_blank');
    if (!printWindow || !responsesData) return;
    
    const grouped: Record<string, ResponseDetail[]> = {};
    for (const r of responsesData.responses) {
      if (!grouped[r.category]) grouped[r.category] = [];
      grouped[r.category].push(r);
    }
    
    let html = `<!DOCTYPE html><html><head><meta charset="utf-8"><title>Risposte Assessment #${responsesData.assessment_id}</title>
    <style>
      body { font-family: 'Courier New', monospace; max-width: 800px; margin: 0 auto; padding: 20px; color: #333; }
      h1 { color: #003366; border-bottom: 2px solid #003366; padding-bottom: 10px; font-size: 18px; }
      h2 { color: #003366; margin-top: 30px; font-size: 16px; background: #f0f4f8; padding: 8px 12px; border-radius: 4px; }
      .question { margin: 15px 0; padding: 12px; border-left: 3px solid #ddd; }
      .question-text { font-weight: bold; margin-bottom: 8px; font-size: 13px; }
      .option { padding: 4px 8px; margin: 2px 0; font-size: 12px; border-radius: 3px; }
      .option.selected { background: #e8f5e9; border: 1px solid #4caf50; font-weight: bold; }
      .option.not-selected { color: #999; }
      .score-badge { display: inline-block; background: #003366; color: white; padding: 2px 8px; border-radius: 10px; font-size: 11px; margin-left: 8px; }
      .summary { background: #f8f9fa; padding: 15px; border-radius: 8px; margin-bottom: 20px; }
      .summary p { margin: 4px 0; font-size: 13px; }
      @media print { body { padding: 0; } }
    </style></head><body>`;
    
    html += `<h1>RISPOSTE ASSESSMENT #${responsesData.assessment_id}</h1>`;
    html += `<div class="summary">`;
    html += `<p><strong>Organizzazione:</strong> ${responsesData.organization.name}</p>`;
    html += `<p><strong>Livello Maturità:</strong> ${responsesData.maturity_level?.toFixed(1) || 'N/A'} / 5</p>`;
    html += `<p><strong>Domande totali:</strong> ${responsesData.total_questions}</p>`;
    if (responsesData.completed_at) html += `<p><strong>Completato:</strong> ${new Date(responsesData.completed_at).toLocaleString('it-IT')}</p>`;
    html += `</div>`;
    
    for (const [category, questions] of Object.entries(grouped)) {
      html += `<h2>${category}</h2>`;
      for (const q of questions) {
        html += `<div class="question">`;
        html += `<div class="question-text">${q.question_text}</div>`;
        for (const opt of q.all_options) {
          const isSelected = opt.text === q.selected_option_text;
          html += `<div class="option ${isSelected ? 'selected' : 'not-selected'}">`;
          html += `${isSelected ? '✔' : '○'} ${opt.text} <span class="score-badge">${opt.score}/5</span></div>`;
        }
        html += `</div>`;
      }
    }
    
    html += `</body></html>`;
    printWindow.document.write(html);
    printWindow.document.close();
    printWindow.print();
  };

  const downloadCVs = async () => {
    try {
      const response = await fetch(`${API_BASE}/admin/staff-cvs?admin_key=${adminKey}`);
      if (response.ok) {
        const data = await response.json();
        const cvs = data.cvs;
        for (const [name, cv] of Object.entries(cvs)) {
          const blob = new Blob([cv as string], { type: 'text/markdown' });
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = `cv-${name}.md`;
          document.body.appendChild(a);
          a.click();
          document.body.removeChild(a);
          URL.revokeObjectURL(url);
        }
      } else {
        alert('Errore nel caricamento dei CV');
      }
    } catch (err) {
      console.error('Error loading CVs:', err);
      alert('Errore di connessione');
    }
  };

  const downloadTimesheet = async () => {
    if (!selectedAssessment) return;
    try {
      const response = await fetch(
        `${API_BASE}/admin/assessments/${selectedAssessment.id}/timesheet?admin_key=${adminKey}`
      );
      if (response.ok) {
        const data = await response.json();
        const blob = new Blob([data.timesheet], { type: 'text/markdown' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `foglio-ore-${data.organization_name || 'assessment'}-${data.assessment_id}.md`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
      } else {
        alert('Errore nella generazione del foglio ore');
      }
    } catch (err) {
      console.error('Error loading timesheet:', err);
      alert('Errore di connessione');
    }
  };

  const downloadFullDocumentation = () => {
    if (!selectedAssessment || !staffProfiles) return;
    
    const fullDoc = `# DOCUMENTAZIONE COMPLETA - DIGITAL MATURITY ASSESSMENT

## Rome Digital Innovation Hub

**Beneficiario:** ${selectedAssessment.organization?.name || 'N/A'}
**Tipologia:** ${selectedAssessment.organization?.type === 'pa' ? 'Pubblica Amministrazione' : 'Impresa'}
**Data:** ${selectedAssessment.completed_at ? new Date(selectedAssessment.completed_at).toLocaleDateString('it-IT') : 'N/A'}

---

# PARTE 1: REPORT DI MATURITÀ DIGITALE

${selectedAssessment.report}

---

# PARTE 2: SCHEDA DI AUDIT

${selectedAssessment.audit_sheet || 'Non disponibile'}

---

# PARTE 3: PROFILI DEL PERSONALE

${staffProfiles.digital_transformation_expert}

---

${staffProfiles.process_innovation_analyst}

---

*Documentazione generata nell'ambito del progetto DIH - Digital Maturity Assessment*
*Data generazione: ${new Date().toLocaleDateString('it-IT')}*
`;
    
    const blob = new Blob([fullDoc], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `documentazione-dih-${selectedAssessment.organization?.name || 'assessment'}-${selectedAssessment.id}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const downloadDocx = async () => {
    if (!selectedAssessment) return;
    
    setGeneratingDoc(true);
    try {
      const children: Paragraph[] = [];
      
      // Header
      children.push(
        new Paragraph({
          children: [new TextRun({ text: 'AUDIT DI MATURITÀ DIGITALE', bold: true, size: 36, color: '003366', font: 'Courier New' })],
          heading: HeadingLevel.TITLE,
          alignment: AlignmentType.CENTER,
        }),
        new Paragraph({
          children: [new TextRun({ text: 'Rome Digital Innovation Hub', size: 24, color: '666666', font: 'Courier New' })],
          alignment: AlignmentType.CENTER,
        }),
        new Paragraph({
          children: [new TextRun({ text: 'in collaborazione con Il Borgo Urbano', size: 22, color: '666666', font: 'Courier New' })],
          alignment: AlignmentType.CENTER,
        }),
        new Paragraph({ text: '' })
      );
      
      // Organization info
      children.push(
        new Paragraph({
          children: [new TextRun({ text: 'DATI ORGANIZZAZIONE', bold: true, size: 28, font: 'Courier New' })],
          heading: HeadingLevel.HEADING_1,
        }),
        new Paragraph({ children: [new TextRun({ text: `Beneficiario: `, bold: true, font: 'Courier New' }), new TextRun({ text: selectedAssessment.organization?.name || '-', font: 'Courier New' })] }),
        new Paragraph({ children: [new TextRun({ text: `Tipologia: `, bold: true, font: 'Courier New' }), new TextRun({ text: selectedAssessment.organization?.type === 'pa' ? 'Pubblica Amministrazione' : 'Impresa', font: 'Courier New' })] }),
        new Paragraph({ children: [new TextRun({ text: `Settore: `, bold: true, font: 'Courier New' }), new TextRun({ text: selectedAssessment.organization?.sector || '-', font: 'Courier New' })] }),
        new Paragraph({ children: [new TextRun({ text: `Dimensione: `, bold: true, font: 'Courier New' }), new TextRun({ text: (selectedAssessment.organization as any)?.size || '-', font: 'Courier New' })] }),
        new Paragraph({ text: '' })
      );
      
      // Maturity level
      children.push(
        new Paragraph({
          children: [new TextRun({ text: 'LIVELLO DI MATURITÀ DIGITALE', bold: true, size: 28, color: '003366', font: 'Courier New' })],
          heading: HeadingLevel.HEADING_1,
        }),
        new Paragraph({
          children: [new TextRun({ text: `Punteggio: ${selectedAssessment.maturity_level?.toFixed(1) || 'N/A'} / 5`, bold: true, size: 32, font: 'Courier New' })],
        }),
        new Paragraph({ text: '' })
      );
      
      // Scores
      if (selectedAssessment.scores && Object.keys(selectedAssessment.scores).length > 0) {
        children.push(
          new Paragraph({
            children: [new TextRun({ text: 'PUNTEGGI PER AREA', bold: true, size: 28, color: '003366', font: 'Courier New' })],
            heading: HeadingLevel.HEADING_1,
          })
        );
        for (const [category, score] of Object.entries(selectedAssessment.scores)) {
          const gap = selectedAssessment.gap_analysis?.[category];
          const priority = gap?.priority || '';
          children.push(
            new Paragraph({
              children: [
                new TextRun({ text: `• ${category}: `, font: 'Courier New' }),
                new TextRun({ text: `${(score as number).toFixed(1)}/5`, bold: true, font: 'Courier New' }),
                new TextRun({ text: priority ? ` (Priorità: ${priority})` : '', font: 'Courier New' }),
              ],
            })
          );
        }
        children.push(new Paragraph({ text: '' }));
      }
      
      // Report content
      if (selectedAssessment.report) {
        children.push(
          new Paragraph({
            children: [new TextRun({ text: 'REPORT COMPLETO', bold: true, size: 28, color: '003366', font: 'Courier New' })],
            heading: HeadingLevel.HEADING_1,
          })
        );
        
        const lines = selectedAssessment.report.split('\n');
        for (const line of lines) {
          const trimmed = line.trim();
          if (!trimmed) {
            children.push(new Paragraph({ text: '' }));
          } else if (trimmed.startsWith('# ')) {
            children.push(new Paragraph({
              children: [new TextRun({ text: trimmed.replace('# ', ''), bold: true, size: 28, color: '003366', font: 'Courier New' })],
              heading: HeadingLevel.HEADING_1,
            }));
          } else if (trimmed.startsWith('## ')) {
            children.push(new Paragraph({
              children: [new TextRun({ text: trimmed.replace('## ', ''), bold: true, size: 24, font: 'Courier New' })],
              heading: HeadingLevel.HEADING_2,
            }));
          } else if (trimmed.startsWith('### ')) {
            children.push(new Paragraph({
              children: [new TextRun({ text: trimmed.replace('### ', ''), bold: true, size: 22, font: 'Courier New' })],
              heading: HeadingLevel.HEADING_3,
            }));
          } else if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
            children.push(new Paragraph({
              children: [new TextRun({ text: `• ${trimmed.substring(2)}`, font: 'Courier New' })],
            }));
          } else if (trimmed.startsWith('> ')) {
            children.push(new Paragraph({
              children: [new TextRun({ text: trimmed.substring(2), italics: true, color: '666666', font: 'Courier New' })],
            }));
          } else if (!trimmed.startsWith('|') && trimmed !== '---') {
            const cleanText = trimmed
              .replace(/\*\*(.*?)\*\*/g, '$1')
              .replace(/\*(.*?)\*/g, '$1')
              .replace(/`(.*?)`/g, '$1');
            children.push(new Paragraph({ children: [new TextRun({ text: cleanText, font: 'Courier New' })] }));
          }
        }
      }
      
      // Footer
      children.push(
        new Paragraph({ text: '' }),
        new Paragraph({
          children: [new TextRun({ text: 'Rome Digital Innovation Hub in collaborazione con Il Borgo Urbano', size: 18, color: '999999', font: 'Courier New' })],
          alignment: AlignmentType.CENTER,
        })
      );
      
      const doc = new Document({
        sections: [{ children }],
        styles: {
          default: {
            document: {
              run: {
                font: 'Courier New',
              },
            },
          },
        },
      });
      
      const blob = await Packer.toBlob(doc);
      saveAs(blob, `report-dih-${selectedAssessment.organization?.name || 'assessment'}-${selectedAssessment.id}.docx`);
    } catch (error) {
      console.error('Error generating DOCX:', error);
    } finally {
      setGeneratingDoc(false);
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
              <div className="flex items-center gap-2 flex-wrap">
                <button
                  onClick={regenerateReport}
                  disabled={regenerating}
                  className="flex items-center gap-2 px-4 py-2 bg-orange-600 text-white rounded-lg hover:bg-orange-700 disabled:opacity-50"
                  title="Rigenera report con nuovo template DIH"
                >
                  {regenerating ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    <BarChart3 className="w-5 h-5" />
                  )}
                  <span className="hidden lg:inline">{regenerating ? 'Rigenerando...' : 'Rigenera Report'}</span>
                </button>
                <button
                  onClick={viewResponses}
                  disabled={loadingResponses}
                  className="flex items-center gap-2 px-4 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 disabled:opacity-50"
                  title="Visualizza risposte dettagliate"
                >
                  {loadingResponses ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    <ListChecks className="w-5 h-5" />
                  )}
                  <span className="hidden lg:inline">Risposte</span>
                </button>
                <button
                  onClick={downloadCVs}
                  className="flex items-center gap-2 px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700"
                  title="Scarica CV figure professionali"
                >
                  <UserCircle className="w-5 h-5" />
                  <span className="hidden lg:inline">CV</span>
                </button>
                <button
                  onClick={downloadTimesheet}
                  className="flex items-center gap-2 px-4 py-2 bg-amber-600 text-white rounded-lg hover:bg-amber-700"
                  title="Scarica foglio ore assessment"
                >
                  <Timer className="w-5 h-5" />
                  <span className="hidden lg:inline">Ore</span>
                </button>
                <button
                  onClick={downloadFullDocumentation}
                  className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white rounded-lg hover:bg-purple-700"
                  title="Scarica tutta la documentazione DIH"
                >
                  <Package className="w-5 h-5" />
                  <span className="hidden lg:inline">Doc. DIH</span>
                </button>
                <button
                  onClick={downloadAuditSheet}
                  disabled={!selectedAssessment.audit_sheet}
                  className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
                  title="Scarica Scheda Audit"
                >
                  <CheckCircle className="w-5 h-5" />
                  <span className="hidden lg:inline">Audit</span>
                </button>
                <button
                  onClick={downloadDocx}
                  disabled={generatingDoc}
                  className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                >
                  {generatingDoc ? (
                    <Loader2 className="w-5 h-5 animate-spin" />
                  ) : (
                    <FileText className="w-5 h-5" />
                  )}
                  <span className="hidden sm:inline">DOCX</span>
                </button>
                <button
                  onClick={downloadReport}
                  className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700"
                >
                  <Download className="w-5 h-5" />
                  <span className="hidden sm:inline">MD</span>
                </button>
              </div>
            </div>
          </div>
        </header>

        <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8" ref={reportRef}>
          {/* Dati Organizzazione */}
          <div className="bg-white rounded-xl shadow-sm p-6 mb-8">
            <h2 className="text-lg font-semibold text-gray-800 mb-4">Dati Organizzazione</h2>
            <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
              <div>
                <p className="text-sm text-gray-500">Ragione Sociale</p>
                <p className="font-semibold text-gray-800">{selectedAssessment.organization?.name || '-'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Tipologia</p>
                <p className="font-semibold text-gray-800">{selectedAssessment.organization?.type === 'pa' ? 'Pubblica Amministrazione' : 'Azienda Privata'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Settore</p>
                <p className="font-semibold text-gray-800">{selectedAssessment.organization?.sector || '-'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Dimensione</p>
                <p className="font-semibold text-gray-800">{(selectedAssessment.organization as any)?.size || '-'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">C.F. / P.IVA</p>
                <p className="font-semibold text-gray-800">{(selectedAssessment.organization as any)?.fiscal_code || '-'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Telefono</p>
                <p className="font-semibold text-gray-800">{(selectedAssessment.organization as any)?.phone || '-'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Email</p>
                <p className="font-semibold text-gray-800">{(selectedAssessment.organization as any)?.email || '-'}</p>
              </div>
              <div>
                <p className="text-sm text-gray-500">Referente</p>
                <p className="font-semibold text-gray-800">{(selectedAssessment.organization as any)?.admin_name || '-'}</p>
              </div>
            </div>
          </div>

          <div className="grid md:grid-cols-3 gap-6 mb-8">
            <div className="bg-white rounded-xl shadow-sm p-6">
              <p className="text-sm text-gray-500 mb-1">Livello Maturità</p>
              <p className="text-4xl font-bold text-primary-600">
                {selectedAssessment.maturity_level?.toFixed(1) || 'N/A'}
                <span className="text-lg text-gray-400"> / 5</span>
              </p>
            </div>
            <div className="bg-white rounded-xl shadow-sm p-6">
              <p className="text-sm text-gray-500 mb-1">Assessment</p>
              <p className="text-xl font-bold text-gray-800">#{selectedAssessment.id}</p>
            </div>
            <div className="bg-white rounded-xl shadow-sm p-6">
              <p className="text-sm text-gray-500 mb-1">Data Completamento</p>
              <p className="text-xl font-bold text-gray-800">
                {selectedAssessment.completed_at 
                  ? new Date(selectedAssessment.completed_at).toLocaleString('it-IT', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Rome' })
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

        {/* Responses Modal */}
        {showResponses && responsesData && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-xl shadow-2xl max-w-4xl w-full max-h-[90vh] flex flex-col">
              <div className="flex items-center justify-between p-6 border-b border-gray-200">
                <div>
                  <h3 className="text-lg font-semibold text-gray-800">
                    Risposte Assessment #{responsesData.assessment_id}
                  </h3>
                  <p className="text-sm text-gray-500">
                    {responsesData.organization.name} — {responsesData.total_questions} domande
                  </p>
                </div>
                <div className="flex items-center gap-2">
                  <button
                    onClick={printResponses}
                    className="flex items-center gap-2 px-3 py-2 bg-teal-600 text-white rounded-lg hover:bg-teal-700 text-sm"
                  >
                    <Printer className="w-4 h-4" />
                    Stampa
                  </button>
                  <button
                    onClick={() => setShowResponses(false)}
                    className="p-2 text-gray-400 hover:text-gray-600"
                  >
                    <X className="w-5 h-5" />
                  </button>
                </div>
              </div>
              <div className="overflow-y-auto p-6">
                {(() => {
                  const grouped: Record<string, ResponseDetail[]> = {};
                  for (const r of responsesData.responses) {
                    if (!grouped[r.category]) grouped[r.category] = [];
                    grouped[r.category].push(r);
                  }
                  return Object.entries(grouped).map(([category, questions]) => (
                    <div key={category} className="mb-6">
                      <h4 className="text-md font-semibold text-white bg-blue-900 px-4 py-2 rounded-lg mb-3">
                        {category}
                      </h4>
                      {questions.map((q) => (
                        <div key={q.question_id} className="mb-4 p-4 border-l-4 border-gray-200 bg-gray-50 rounded-r-lg">
                          <p className="font-medium text-gray-800 text-sm mb-2">{q.question_text}</p>
                          <div className="space-y-1">
                            {q.all_options.map((opt, idx) => {
                              const isSelected = opt.text === q.selected_option_text;
                              return (
                                <div
                                  key={idx}
                                  className={`flex items-center justify-between px-3 py-1.5 rounded text-sm ${
                                    isSelected
                                      ? 'bg-green-100 border border-green-400 font-semibold text-green-800'
                                      : 'text-gray-400'
                                  }`}
                                >
                                  <span>{isSelected ? '✔' : '○'} {opt.text}</span>
                                  <span className={`text-xs px-2 py-0.5 rounded-full ${
                                    isSelected ? 'bg-green-600 text-white' : 'bg-gray-200 text-gray-500'
                                  }`}>
                                    {opt.score}/5
                                  </span>
                                </div>
                              );
                            })}
                          </div>
                        </div>
                      ))}
                    </div>
                  ));
                })()}
              </div>
            </div>
          </div>
        )}
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
                        Registrato: {org.created_at ? new Date(org.created_at).toLocaleString('it-IT', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Rome' }) : 'N/A'}
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
                                {(assessment as any).level === 2 ? 'Assessment 2' : 'Assessment 1'} <span className="text-gray-400">#{assessment.id}</span>
                              </p>
                              <p className="text-xs text-gray-500">
                                {assessment.created_at 
                                  ? new Date(assessment.created_at).toLocaleString('it-IT', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Rome' })
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
