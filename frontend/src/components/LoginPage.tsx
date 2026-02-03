import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Lock, Building2, ArrowRight, UserPlus } from 'lucide-react';
import { authApi } from '../api';
import { useAuth } from '../context/AuthContext';

const LoginPage: React.FC = () => {
  const [isLogin, setIsLogin] = useState(true);
  const [accessCode, setAccessCode] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [type, setType] = useState('azienda');
  const [sector, setSector] = useState('');
  const [size, setSize] = useState('');
  const [email, setEmail] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const [showAccessCode, setShowAccessCode] = useState(false);
  const [newAccessCode, setNewAccessCode] = useState('');

  const navigate = useNavigate();
  const { login } = useAuth();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await authApi.login(accessCode, password);
      login(response.access_token, response.organization);
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Errore durante il login');
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const response = await authApi.register({
        name,
        type,
        sector: sector || undefined,
        size: size || undefined,
        email: email || undefined,
        password,
      });
      setNewAccessCode(response.organization.access_code);
      setShowAccessCode(true);
      login(response.access_token, response.organization);
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Errore durante la registrazione');
    } finally {
      setLoading(false);
    }
  };

  if (showAccessCode) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-primary-600 to-primary-900 flex items-center justify-center p-4">
        <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full animate-fade-in">
          <div className="text-center">
            <div className="w-20 h-20 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-6">
              <svg className="w-10 h-10 text-green-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-gray-800 mb-2">Registrazione Completata!</h2>
            <p className="text-gray-600 mb-6">Salva il tuo codice di accesso per i prossimi login:</p>
            <div className="bg-primary-50 border-2 border-primary-200 rounded-xl p-6 mb-6">
              <p className="text-sm text-primary-600 mb-2">Il tuo codice di accesso</p>
              <p className="text-4xl font-mono font-bold text-primary-700 tracking-wider">{newAccessCode}</p>
            </div>
            <p className="text-sm text-gray-500 mb-6">
              Questo codice sarà necessario per accedere al sistema dal tuo tablet kiosk.
            </p>
            <button
              onClick={() => navigate('/dashboard')}
              className="w-full bg-primary-600 text-white py-4 rounded-xl font-semibold hover:bg-primary-700 transition-colors flex items-center justify-center gap-2"
            >
              Vai alla Dashboard
              <ArrowRight className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-600 to-primary-900 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-2xl p-8 max-w-md w-full animate-fade-in">
        <div className="text-center mb-8">
          <div className="w-20 h-20 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
            <Building2 className="w-10 h-10 text-primary-600" />
          </div>
          <h1 className="text-2xl font-bold text-gray-800">Valutazione Maturità Digitale</h1>
          <p className="text-gray-500 mt-2">Per Aziende e Pubbliche Amministrazioni</p>
        </div>

        <div className="flex mb-6 bg-gray-100 rounded-xl p-1">
          <button
            onClick={() => setIsLogin(true)}
            className={`flex-1 py-3 rounded-lg font-medium transition-all ${
              isLogin ? 'bg-white shadow text-primary-600' : 'text-gray-500'
            }`}
          >
            Accedi
          </button>
          <button
            onClick={() => setIsLogin(false)}
            className={`flex-1 py-3 rounded-lg font-medium transition-all ${
              !isLogin ? 'bg-white shadow text-primary-600' : 'text-gray-500'
            }`}
          >
            Registrati
          </button>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-xl mb-6">
            {error}
          </div>
        )}

        {isLogin ? (
          <form onSubmit={handleLogin} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Codice di Accesso
              </label>
              <div className="relative">
                <Lock className="absolute left-4 top-1/2 transform -translate-y-1/2 text-gray-400 w-5 h-5" />
                <input
                  type="text"
                  value={accessCode}
                  onChange={(e) => setAccessCode(e.target.value.toUpperCase())}
                  className="w-full pl-12 pr-4 py-4 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent text-lg font-mono tracking-wider"
                  placeholder="XXXXXXXX"
                  required
                />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-4 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="••••••••"
                required
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-primary-600 text-white py-4 rounded-xl font-semibold hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {loading ? (
                <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <>
                  Accedi
                  <ArrowRight className="w-5 h-5" />
                </>
              )}
            </button>
          </form>
        ) : (
          <form onSubmit={handleRegister} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Nome Organizzazione *
              </label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="Es. Comune di Roma"
                required
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Tipologia *
              </label>
              <select
                value={type}
                onChange={(e) => setType(e.target.value)}
                className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
                <option value="azienda">Azienda Privata</option>
                <option value="pa">Pubblica Amministrazione</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Settore
              </label>
              <input
                type="text"
                value={sector}
                onChange={(e) => setSector(e.target.value)}
                className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="Es. Manifatturiero, Servizi, Sanità..."
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Dimensione
              </label>
              <select
                value={size}
                onChange={(e) => setSize(e.target.value)}
                className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent"
              >
                <option value="">Seleziona...</option>
                <option value="micro">Micro (1-9 dipendenti)</option>
                <option value="piccola">Piccola (10-49 dipendenti)</option>
                <option value="media">Media (50-249 dipendenti)</option>
                <option value="grande">Grande (250+ dipendenti)</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Email
              </label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="email@organizzazione.it"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Password *
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 border border-gray-200 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent"
                placeholder="Minimo 8 caratteri"
                minLength={8}
                required
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-primary-600 text-white py-4 rounded-xl font-semibold hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
            >
              {loading ? (
                <div className="w-6 h-6 border-2 border-white border-t-transparent rounded-full animate-spin" />
              ) : (
                <>
                  <UserPlus className="w-5 h-5" />
                  Registra Organizzazione
                </>
              )}
            </button>
          </form>
        )}
      </div>
    </div>
  );
};

export default LoginPage;
