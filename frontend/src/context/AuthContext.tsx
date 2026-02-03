import React, { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { Organization, AuthState } from '../types';

interface AuthContextType extends AuthState {
  login: (token: string, organization: Organization) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [authState, setAuthState] = useState<AuthState>({
    token: null,
    organization: null,
    isAuthenticated: false,
  });

  useEffect(() => {
    const token = localStorage.getItem('token');
    const orgStr = localStorage.getItem('organization');
    
    if (token && orgStr) {
      try {
        const organization = JSON.parse(orgStr);
        setAuthState({
          token,
          organization,
          isAuthenticated: true,
        });
      } catch {
        localStorage.removeItem('token');
        localStorage.removeItem('organization');
      }
    }
  }, []);

  const login = (token: string, organization: Organization) => {
    localStorage.setItem('token', token);
    localStorage.setItem('organization', JSON.stringify(organization));
    setAuthState({
      token,
      organization,
      isAuthenticated: true,
    });
  };

  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('organization');
    setAuthState({
      token: null,
      organization: null,
      isAuthenticated: false,
    });
  };

  return (
    <AuthContext.Provider value={{ ...authState, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};
