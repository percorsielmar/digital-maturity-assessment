import React, { useEffect, useState, useRef } from 'react';
import { useParams, useNavigate, useSearchParams } from 'react-router-dom';
import { 
  Home, 
  Download, 
  BarChart3,
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  ArrowLeft,
  FileText
} from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { Document, Packer, Paragraph, TextRun, HeadingLevel, AlignmentType } from 'docx';
import { saveAs } from 'file-saver';
import { 
  RadarChart, 
  PolarGrid, 
  PolarAngleAxis, 
  PolarRadiusAxis, 
  Radar, 
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Cell
} from 'recharts';
import { assessmentsApi } from '../api';
import { useAuth } from '../context/AuthContext';

interface ReportData {
  report: string;
  audit_sheet?: string;
  scores: Record<string, number>;
  maturity_level: number;
  gap_analysis: Record<string, {
    current_score: number;
    target_score: number;
    gap: number;
    priority: string;
  }>;
}

interface StaffProfiles {
  digital_transformation_expert: string;
  process_innovation_analyst: string;
}

const ReportPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  const { organization } = useAuth();
  const [reportData, setReportData] = useState<ReportData | null>(null);
  const [staffProfiles, setStaffProfiles] = useState<StaffProfiles | null>(null);
  const [loading, setLoading] = useState(true);
  const [activeTab, setActiveTab] = useState<'overview' | 'details' | 'report' | 'audit' | 'staff'>('overview');
  const [generatingDoc, setGeneratingDoc] = useState(false);
  const [autoDownloadTriggered, setAutoDownloadTriggered] = useState(false);
  const reportRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    loadReport();
  }, [id]);

  useEffect(() => {
    if (searchParams.get('download') === 'docx' && reportData && !loading && !autoDownloadTriggered) {
      setAutoDownloadTriggered(true);
      setTimeout(() => {
        handleDownloadDocx();
      }, 500);
    }
  }, [searchParams, reportData, loading, autoDownloadTriggered]);

  const loadReport = async () => {
    if (!id) return;
    try {
      const [reportResponse, profilesResponse] = await Promise.all([
        assessmentsApi.getReport(parseInt(id)),
        assessmentsApi.getStaffProfiles()
      ]);
      setReportData(reportResponse);
      setStaffProfiles(profilesResponse.profiles);
    } catch (error) {
      console.error('Error loading report:', error);
    } finally {
      setLoading(false);
    }
  };

  const getMaturityLabel = (level: number) => {
    if (level < 2) return { label: 'Iniziale', color: 'text-red-600', bg: 'bg-red-100' };
    if (level < 3) return { label: 'Gestito', color: 'text-orange-600', bg: 'bg-orange-100' };
    if (level < 4) return { label: 'Definito', color: 'text-yellow-600', bg: 'bg-yellow-100' };
    if (level < 4.5) return { label: 'Avanzato', color: 'text-blue-600', bg: 'bg-blue-100' };
    return { label: 'Ottimizzato', color: 'text-green-600', bg: 'bg-green-100' };
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'Alta': return '#ef4444';
      case 'Media': return '#f59e0b';
      case 'Bassa': return '#22c55e';
      default: return '#6b7280';
    }
  };

  const handleDownloadReport = () => {
    if (!reportData) return;
    
    const blob = new Blob([reportData.report], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `report-dih-${organization?.name || 'assessment'}-${id}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleDownloadAuditSheet = () => {
    if (!reportData?.audit_sheet) return;
    
    const blob = new Blob([reportData.audit_sheet], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `scheda-audit-${organization?.name || 'assessment'}-${id}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleDownloadStaffProfiles = () => {
    if (!staffProfiles) return;
    
    const content = `# SCHEDE PROFILO PERSONALE DIH

---

${staffProfiles.digital_transformation_expert}

---

${staffProfiles.process_innovation_analyst}

---

*Rome Digital Innovation Hub - Programma Digital Maturity Assessment*
`;
    
    const blob = new Blob([content], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `profili-staff-dih.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleDownloadFullDocumentation = () => {
    if (!reportData || !staffProfiles) return;
    
    const fullDoc = `# DOCUMENTAZIONE COMPLETA - DIGITAL MATURITY ASSESSMENT

## Rome Digital Innovation Hub

---

# PARTE 1: REPORT DI MATURITÀ DIGITALE

${reportData.report}

---

# PARTE 2: SCHEDA DI AUDIT

${reportData.audit_sheet || 'Non disponibile'}

---

# PARTE 3: PROFILI DEL PERSONALE

${staffProfiles.digital_transformation_expert}

---

${staffProfiles.process_innovation_analyst}

---

*Documentazione generata nell'ambito del progetto DIH - Digital Maturity Assessment*
*Data: ${new Date().toLocaleDateString('it-IT')}*
`;
    
    const blob = new Blob([fullDoc], { type: 'text/markdown' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `documentazione-completa-dih-${organization?.name || 'assessment'}-${id}.md`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  };

  const handleDownloadDocx = async () => {
    if (!reportData) return;
    
    setGeneratingDoc(true);
    try {
      const children: Paragraph[] = [];
      
      // Header
      children.push(
        new Paragraph({
          children: [new TextRun({ text: 'AUDIT DI MATURITÀ DIGITALE', bold: true, size: 36, color: '003366' })],
          heading: HeadingLevel.TITLE,
          alignment: AlignmentType.CENTER,
        }),
        new Paragraph({
          children: [new TextRun({ text: 'Rome Digital Innovation Hub', size: 24, color: '666666' })],
          alignment: AlignmentType.CENTER,
        }),
        new Paragraph({ text: '' })
      );
      
      // Organization info
      children.push(
        new Paragraph({
          children: [new TextRun({ text: 'DATI ORGANIZZAZIONE', bold: true, size: 28 })],
          heading: HeadingLevel.HEADING_1,
        }),
        new Paragraph({ children: [new TextRun({ text: `Beneficiario: `, bold: true }), new TextRun({ text: organization?.name || '-' })] }),
        new Paragraph({ children: [new TextRun({ text: `Tipologia: `, bold: true }), new TextRun({ text: organization?.type === 'pa' ? 'Pubblica Amministrazione' : 'Impresa' })] }),
        new Paragraph({ children: [new TextRun({ text: `Settore: `, bold: true }), new TextRun({ text: organization?.sector || '-' })] }),
        new Paragraph({ children: [new TextRun({ text: `Dimensione: `, bold: true }), new TextRun({ text: organization?.size || '-' })] }),
        new Paragraph({ children: [new TextRun({ text: `Data: `, bold: true }), new TextRun({ text: new Date().toLocaleDateString('it-IT') })] }),
        new Paragraph({ text: '' })
      );
      
      // Maturity level
      children.push(
        new Paragraph({
          children: [new TextRun({ text: 'LIVELLO DI MATURITÀ DIGITALE', bold: true, size: 28, color: '003366' })],
          heading: HeadingLevel.HEADING_1,
        }),
        new Paragraph({
          children: [new TextRun({ text: `Punteggio: ${reportData.maturity_level?.toFixed(1) || 'N/A'} / 5`, bold: true, size: 32 })],
        }),
        new Paragraph({ text: '' })
      );
      
      // Scores
      if (reportData.scores && Object.keys(reportData.scores).length > 0) {
        children.push(
          new Paragraph({
            children: [new TextRun({ text: 'PUNTEGGI PER AREA', bold: true, size: 28, color: '003366' })],
            heading: HeadingLevel.HEADING_1,
          })
        );
        for (const [category, score] of Object.entries(reportData.scores)) {
          const gap = reportData.gap_analysis?.[category];
          const priority = gap?.priority || '';
          children.push(
            new Paragraph({
              children: [
                new TextRun({ text: `• ${category}: ` }),
                new TextRun({ text: `${score.toFixed(1)}/5`, bold: true }),
                new TextRun({ text: priority ? ` (Priorità: ${priority})` : '' }),
              ],
            })
          );
        }
        children.push(new Paragraph({ text: '' }));
      }
      
      // Report content
      if (reportData.report) {
        children.push(
          new Paragraph({
            children: [new TextRun({ text: 'REPORT COMPLETO', bold: true, size: 28, color: '003366' })],
            heading: HeadingLevel.HEADING_1,
          })
        );
        
        const lines = reportData.report.split('\n');
        for (const line of lines) {
          const trimmed = line.trim();
          if (!trimmed) {
            children.push(new Paragraph({ text: '' }));
          } else if (trimmed.startsWith('# ')) {
            children.push(new Paragraph({
              children: [new TextRun({ text: trimmed.replace('# ', ''), bold: true, size: 28, color: '003366' })],
              heading: HeadingLevel.HEADING_1,
            }));
          } else if (trimmed.startsWith('## ')) {
            children.push(new Paragraph({
              children: [new TextRun({ text: trimmed.replace('## ', ''), bold: true, size: 24 })],
              heading: HeadingLevel.HEADING_2,
            }));
          } else if (trimmed.startsWith('### ')) {
            children.push(new Paragraph({
              children: [new TextRun({ text: trimmed.replace('### ', ''), bold: true, size: 22 })],
              heading: HeadingLevel.HEADING_3,
            }));
          } else if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
            children.push(new Paragraph({
              children: [new TextRun({ text: `• ${trimmed.substring(2)}` })],
            }));
          } else if (trimmed.startsWith('> ')) {
            children.push(new Paragraph({
              children: [new TextRun({ text: trimmed.substring(2), italics: true, color: '666666' })],
            }));
          } else if (!trimmed.startsWith('|') && trimmed !== '---') {
            const cleanText = trimmed
              .replace(/\*\*(.*?)\*\*/g, '$1')
              .replace(/\*(.*?)\*/g, '$1')
              .replace(/`(.*?)`/g, '$1');
            children.push(new Paragraph({ text: cleanText }));
          }
        }
      }
      
      // Footer
      children.push(
        new Paragraph({ text: '' }),
        new Paragraph({
          children: [new TextRun({ text: 'Rome Digital Innovation Hub - Programma di Trasformazione Digitale', size: 18, color: '999999' })],
          alignment: AlignmentType.CENTER,
        }),
        new Paragraph({
          children: [new TextRun({ text: `Documento generato il ${new Date().toLocaleDateString('it-IT')}`, size: 18, color: '999999' })],
          alignment: AlignmentType.CENTER,
        })
      );
      
      const doc = new Document({
        sections: [{ children }],
      });
      
      const blob = await Packer.toBlob(doc);
      saveAs(blob, `report-dih-${organization?.name || 'assessment'}-${id}.docx`);
    } catch (error) {
      console.error('Error generating DOCX:', error);
    } finally {
      setGeneratingDoc(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="w-16 h-16 border-4 border-primary-200 border-t-primary-600 rounded-full animate-spin" />
      </div>
    );
  }

  if (!reportData) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-gray-500 mb-4">Report non disponibile</p>
          <button
            onClick={() => navigate('/dashboard')}
            className="text-primary-600 hover:text-primary-700"
          >
            Torna alla Dashboard
          </button>
        </div>
      </div>
    );
  }

  const maturityInfo = getMaturityLabel(reportData.maturity_level);
  
  const radarData = Object.entries(reportData.scores).map(([category, score]) => ({
    category: category.split(' ').slice(0, 2).join(' '),
    fullCategory: category,
    score,
    fullMark: 5
  }));

  const barData = Object.entries(reportData.gap_analysis).map(([category, data]) => ({
    category: category.split(' ').slice(0, 2).join(' '),
    fullCategory: category,
    score: data.current_score,
    gap: data.gap,
    priority: data.priority
  }));

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-4">
              <button
                onClick={() => navigate('/dashboard')}
                className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <ArrowLeft className="w-5 h-5" />
              </button>
              <div>
                <h1 className="text-xl font-bold text-gray-800">Report di Maturità Digitale</h1>
                <p className="text-sm text-gray-500">{organization?.name}</p>
              </div>
            </div>
            <div className="flex items-center gap-2">
              <button
                onClick={handleDownloadFullDocumentation}
                className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white hover:bg-green-700 rounded-lg transition-colors"
                title="Scarica tutta la documentazione DIH"
              >
                <Download className="w-5 h-5" />
                <span className="hidden lg:inline">Documentazione DIH</span>
              </button>
              <button
                onClick={handleDownloadDocx}
                disabled={generatingDoc}
                className="flex items-center gap-2 px-4 py-2 bg-primary-600 text-white hover:bg-primary-700 rounded-lg transition-colors disabled:opacity-50"
              >
                {generatingDoc ? (
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                ) : (
                  <FileText className="w-5 h-5" />
                )}
                <span className="hidden sm:inline">{generatingDoc ? 'Generando...' : 'DOCX'}</span>
              </button>
              <button
                onClick={() => navigate('/dashboard')}
                className="flex items-center gap-2 px-4 py-2 text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
              >
                <Home className="w-5 h-5" />
              </button>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8" ref={reportRef}>
        {/* Dati Aziendali */}
        <div className="bg-white rounded-2xl shadow-lg p-6 mb-8">
          <h2 className="text-lg font-bold text-gray-800 mb-4">Dati Organizzazione</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            <div>
              <p className="text-sm text-gray-500">Ragione Sociale</p>
              <p className="font-semibold text-gray-800">{organization?.name || '-'}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Tipologia</p>
              <p className="font-semibold text-gray-800">{organization?.type === 'pa' ? 'Pubblica Amministrazione' : 'Azienda Privata'}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Settore</p>
              <p className="font-semibold text-gray-800">{organization?.sector || '-'}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Dimensione</p>
              <p className="font-semibold text-gray-800">{organization?.size || '-'}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">C.F. / P.IVA</p>
              <p className="font-semibold text-gray-800">{organization?.fiscal_code || '-'}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Telefono</p>
              <p className="font-semibold text-gray-800">{organization?.phone || '-'}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Email</p>
              <p className="font-semibold text-gray-800">{organization?.email || '-'}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Referente Compilazione</p>
              <p className="font-semibold text-gray-800">{organization?.admin_name || '-'}</p>
            </div>
            <div>
              <p className="text-sm text-gray-500">Data Assessment</p>
              <p className="font-semibold text-gray-800">{new Date().toLocaleString('it-IT', { day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', timeZone: 'Europe/Rome' })}</p>
            </div>
          </div>
        </div>

        <div className="bg-gradient-to-br from-primary-600 to-primary-800 rounded-2xl p-8 mb-8 text-white">
          <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-6">
            <div>
              <p className="text-primary-200 mb-2">Livello di Maturità Digitale</p>
              <div className="flex items-baseline gap-4">
                <span className="text-6xl font-bold">{reportData.maturity_level.toFixed(1)}</span>
                <span className="text-2xl text-primary-200">/ 5</span>
              </div>
              <div className={`inline-block mt-4 px-4 py-2 rounded-full ${maturityInfo.bg} ${maturityInfo.color} font-semibold`}>
                {maturityInfo.label}
              </div>
            </div>
            <div className="w-48 h-48">
              <ResponsiveContainer width="100%" height="100%">
                <RadarChart data={radarData}>
                  <PolarGrid stroke="rgba(255,255,255,0.3)" />
                  <PolarAngleAxis dataKey="category" tick={{ fill: 'white', fontSize: 10 }} />
                  <PolarRadiusAxis angle={30} domain={[0, 5]} tick={{ fill: 'white' }} />
                  <Radar
                    name="Score"
                    dataKey="score"
                    stroke="#fff"
                    fill="rgba(255,255,255,0.3)"
                    fillOpacity={0.6}
                  />
                </RadarChart>
              </ResponsiveContainer>
            </div>
          </div>
        </div>

        <div className="flex flex-wrap gap-2 mb-6 bg-white rounded-xl p-1 shadow-sm">
          <button
            onClick={() => setActiveTab('overview')}
            className={`flex-1 min-w-[120px] flex items-center justify-center gap-2 py-3 rounded-lg font-medium transition-all ${
              activeTab === 'overview' ? 'bg-primary-100 text-primary-700' : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            <BarChart3 className="w-5 h-5" />
            <span className="hidden sm:inline">Panoramica</span>
          </button>
          <button
            onClick={() => setActiveTab('details')}
            className={`flex-1 min-w-[120px] flex items-center justify-center gap-2 py-3 rounded-lg font-medium transition-all ${
              activeTab === 'details' ? 'bg-primary-100 text-primary-700' : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            <TrendingUp className="w-5 h-5" />
            <span className="hidden sm:inline">Gap Analysis</span>
          </button>
          <button
            onClick={() => setActiveTab('report')}
            className={`flex-1 min-w-[120px] flex items-center justify-center gap-2 py-3 rounded-lg font-medium transition-all ${
              activeTab === 'report' ? 'bg-primary-100 text-primary-700' : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            <FileText className="w-5 h-5" />
            <span className="hidden sm:inline">Report DIH</span>
          </button>
          <button
            onClick={() => setActiveTab('audit')}
            className={`flex-1 min-w-[120px] flex items-center justify-center gap-2 py-3 rounded-lg font-medium transition-all ${
              activeTab === 'audit' ? 'bg-green-100 text-green-700' : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            <CheckCircle className="w-5 h-5" />
            <span className="hidden sm:inline">Scheda Audit</span>
          </button>
          <button
            onClick={() => setActiveTab('staff')}
            className={`flex-1 min-w-[120px] flex items-center justify-center gap-2 py-3 rounded-lg font-medium transition-all ${
              activeTab === 'staff' ? 'bg-purple-100 text-purple-700' : 'text-gray-500 hover:text-gray-700'
            }`}
          >
            <AlertTriangle className="w-5 h-5" />
            <span className="hidden sm:inline">Profili Staff</span>
          </button>
        </div>

        {activeTab === 'overview' && (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 animate-fade-in">
            {Object.entries(reportData.scores).map(([category, score]) => {
              const gap = reportData.gap_analysis[category];
              return (
                <div key={category} className="bg-white rounded-xl shadow-sm p-6 border border-gray-100">
                  <div className="flex items-start justify-between mb-4">
                    <h3 className="font-semibold text-gray-800">{category}</h3>
                    {gap && (
                      <span 
                        className="px-2 py-1 rounded-full text-xs font-medium"
                        style={{ 
                          backgroundColor: `${getPriorityColor(gap.priority)}20`,
                          color: getPriorityColor(gap.priority)
                        }}
                      >
                        {gap.priority}
                      </span>
                    )}
                  </div>
                  <div className="flex items-end gap-2 mb-4">
                    <span className="text-4xl font-bold text-primary-600">{score.toFixed(1)}</span>
                    <span className="text-gray-400 mb-1">/ 5</span>
                  </div>
                  <div className="w-full bg-gray-100 rounded-full h-2">
                    <div 
                      className="bg-primary-500 h-2 rounded-full transition-all"
                      style={{ width: `${(score / 5) * 100}%` }}
                    />
                  </div>
                  {gap && (
                    <p className="text-sm text-gray-500 mt-3">
                      Gap: <span className="font-medium">{gap.gap.toFixed(1)}</span> punti
                    </p>
                  )}
                </div>
              );
            })}
          </div>
        )}

        {activeTab === 'details' && (
          <div className="animate-fade-in">
            <div className="bg-white rounded-xl shadow-sm p-6 mb-6">
              <h3 className="font-semibold text-gray-800 mb-6">Gap Analysis per Categoria</h3>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={barData} layout="vertical">
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" domain={[0, 5]} />
                    <YAxis dataKey="category" type="category" width={100} tick={{ fontSize: 12 }} />
                    <Tooltip 
                      formatter={(value: number, name: string) => [value.toFixed(2), name === 'score' ? 'Punteggio' : 'Gap']}
                      labelFormatter={(label) => barData.find(d => d.category === label)?.fullCategory || label}
                    />
                    <Bar dataKey="score" name="Punteggio" stackId="a">
                      {barData.map((_, index) => (
                        <Cell key={`cell-${index}`} fill="#3b82f6" />
                      ))}
                    </Bar>
                    <Bar dataKey="gap" name="Gap" stackId="a">
                      {barData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={getPriorityColor(entry.priority)} opacity={0.5} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            <div className="grid md:grid-cols-3 gap-6">
              <div className="bg-white rounded-xl shadow-sm p-6 border-l-4 border-red-500">
                <div className="flex items-center gap-3 mb-4">
                  <AlertTriangle className="w-6 h-6 text-red-500" />
                  <h3 className="font-semibold text-gray-800">Priorità Alta</h3>
                </div>
                <ul className="space-y-2">
                  {Object.entries(reportData.gap_analysis)
                    .filter(([_, data]) => data.priority === 'Alta')
                    .map(([category]) => (
                      <li key={category} className="text-sm text-gray-600 flex items-center gap-2">
                        <span className="w-2 h-2 bg-red-500 rounded-full" />
                        {category}
                      </li>
                    ))}
                  {Object.entries(reportData.gap_analysis).filter(([_, data]) => data.priority === 'Alta').length === 0 && (
                    <li className="text-sm text-gray-400">Nessuna area critica</li>
                  )}
                </ul>
              </div>

              <div className="bg-white rounded-xl shadow-sm p-6 border-l-4 border-yellow-500">
                <div className="flex items-center gap-3 mb-4">
                  <TrendingUp className="w-6 h-6 text-yellow-500" />
                  <h3 className="font-semibold text-gray-800">Priorità Media</h3>
                </div>
                <ul className="space-y-2">
                  {Object.entries(reportData.gap_analysis)
                    .filter(([_, data]) => data.priority === 'Media')
                    .map(([category]) => (
                      <li key={category} className="text-sm text-gray-600 flex items-center gap-2">
                        <span className="w-2 h-2 bg-yellow-500 rounded-full" />
                        {category}
                      </li>
                    ))}
                  {Object.entries(reportData.gap_analysis).filter(([_, data]) => data.priority === 'Media').length === 0 && (
                    <li className="text-sm text-gray-400">Nessuna area</li>
                  )}
                </ul>
              </div>

              <div className="bg-white rounded-xl shadow-sm p-6 border-l-4 border-green-500">
                <div className="flex items-center gap-3 mb-4">
                  <CheckCircle className="w-6 h-6 text-green-500" />
                  <h3 className="font-semibold text-gray-800">Priorità Bassa</h3>
                </div>
                <ul className="space-y-2">
                  {Object.entries(reportData.gap_analysis)
                    .filter(([_, data]) => data.priority === 'Bassa')
                    .map(([category]) => (
                      <li key={category} className="text-sm text-gray-600 flex items-center gap-2">
                        <span className="w-2 h-2 bg-green-500 rounded-full" />
                        {category}
                      </li>
                    ))}
                  {Object.entries(reportData.gap_analysis).filter(([_, data]) => data.priority === 'Bassa').length === 0 && (
                    <li className="text-sm text-gray-400">Nessuna area</li>
                  )}
                </ul>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'report' && (
          <div className="bg-white rounded-xl shadow-sm p-8 animate-fade-in">
            <div className="flex justify-end mb-4">
              <button
                onClick={handleDownloadReport}
                className="flex items-center gap-2 px-4 py-2 text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
              >
                <Download className="w-5 h-5" />
                Scarica Report MD
              </button>
            </div>
            <div className="prose prose-lg max-w-none">
              <ReactMarkdown>{reportData.report}</ReactMarkdown>
            </div>
          </div>
        )}

        {activeTab === 'audit' && (
          <div className="bg-white rounded-xl shadow-sm p-8 animate-fade-in">
            <div className="flex justify-between items-center mb-6">
              <div>
                <h2 className="text-xl font-bold text-gray-800">Scheda di Audit</h2>
                <p className="text-sm text-gray-500">Documento per rendicontazione UE - Rome DIH</p>
              </div>
              <button
                onClick={handleDownloadAuditSheet}
                className="flex items-center gap-2 px-4 py-2 bg-green-600 text-white hover:bg-green-700 rounded-lg transition-colors"
              >
                <Download className="w-5 h-5" />
                Scarica Scheda Audit
              </button>
            </div>
            {reportData.audit_sheet ? (
              <div className="prose prose-lg max-w-none">
                <ReactMarkdown>{reportData.audit_sheet}</ReactMarkdown>
              </div>
            ) : (
              <div className="text-center py-12 text-gray-500">
                <FileText className="w-12 h-12 mx-auto mb-4 opacity-50" />
                <p>Scheda di Audit non disponibile per questo assessment.</p>
                <p className="text-sm mt-2">La scheda viene generata automaticamente per i nuovi assessment.</p>
              </div>
            )}
          </div>
        )}

        {activeTab === 'staff' && (
          <div className="animate-fade-in space-y-6">
            <div className="flex justify-between items-center">
              <div>
                <h2 className="text-xl font-bold text-gray-800">Profili del Personale DIH</h2>
                <p className="text-sm text-gray-500">Schede profilo per rendicontazione costi personale</p>
              </div>
              <button
                onClick={handleDownloadStaffProfiles}
                className="flex items-center gap-2 px-4 py-2 bg-purple-600 text-white hover:bg-purple-700 rounded-lg transition-colors"
              >
                <Download className="w-5 h-5" />
                Scarica Profili Staff
              </button>
            </div>
            
            {staffProfiles ? (
              <>
                <div className="bg-white rounded-xl shadow-sm p-8 border-l-4 border-blue-500">
                  <div className="prose prose-lg max-w-none">
                    <ReactMarkdown>{staffProfiles.digital_transformation_expert}</ReactMarkdown>
                  </div>
                </div>
                
                <div className="bg-white rounded-xl shadow-sm p-8 border-l-4 border-purple-500">
                  <div className="prose prose-lg max-w-none">
                    <ReactMarkdown>{staffProfiles.process_innovation_analyst}</ReactMarkdown>
                  </div>
                </div>
              </>
            ) : (
              <div className="bg-white rounded-xl shadow-sm p-12 text-center text-gray-500">
                <AlertTriangle className="w-12 h-12 mx-auto mb-4 opacity-50" />
                <p>Profili del personale non disponibili.</p>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
};

export default ReportPage;
