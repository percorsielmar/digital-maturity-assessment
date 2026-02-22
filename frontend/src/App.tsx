import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import LoginPage from './components/LoginPage';
import Dashboard from './components/Dashboard';
import AssessmentPage from './components/AssessmentPage';
import AssessmentLevel2Page from './components/AssessmentLevel2Page';
import ReportPage from './components/ReportPage';
import AdminPage from './components/AdminPage';
import LandingPage from './components/LandingPage';

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated } = useAuth();
  
  if (!isAuthenticated) {
    return <Navigate to="/" replace />;
  }
  
  return <>{children}</>;
};

const App: React.FC = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/maturita-digitale" element={<LoginPage />} />
          <Route path="/iso56002" element={
            <LoginPage
              program="iso56002"
              title="Audit Propedeutico UNI/PdR 56002"
              subtitle="Gestione dell'Innovazione — Assessment di Conformità"
              gradientFrom="from-emerald-600"
              gradientTo="to-emerald-900"
            />
          } />
          <Route path="/governance" element={
            <LoginPage
              program="governance"
              title="Governance Trasparente"
              subtitle="Formazione e Consulenza per la PA"
              gradientFrom="from-amber-600"
              gradientTo="to-amber-900"
              defaultType="pa"
              showTypeSelector={false}
            />
          } />
          <Route path="/patto-di-senso" element={
            <LoginPage
              program="patto_di_senso"
              title="Patto di Senso"
              subtitle="Audit di Maturità — Innovazione Sociale e Territoriale"
              gradientFrom="from-pink-500"
              gradientTo="to-pink-900"
            />
          } />
          <Route path="/admin" element={<AdminPage />} />
          <Route
            path="/dashboard"
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            }
          />
          <Route
            path="/assessment/:id"
            element={
              <ProtectedRoute>
                <AssessmentPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/report/:id"
            element={
              <ProtectedRoute>
                <ReportPage />
              </ProtectedRoute>
            }
          />
          <Route
            path="/assessment-level2/:id"
            element={
              <ProtectedRoute>
                <AssessmentLevel2Page />
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;
