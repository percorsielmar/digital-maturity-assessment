import axios from 'axios';
import { Organization, Question, Assessment, Answer, Level2Question } from './types';

const API_BASE = import.meta.env.VITE_API_URL || '/api';

const api = axios.create({
  baseURL: API_BASE,
  timeout: 60000, // 60 seconds timeout for slow backend wake-up
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('organization');
      window.location.href = '/';
    }
    return Promise.reject(error);
  }
);

export const authApi = {
  register: async (data: {
    name: string;
    type: string;
    sector?: string;
    size?: string;
    email?: string;
    fiscal_code?: string;
    phone?: string;
    admin_name?: string;
    password: string;
  }) => {
    const response = await api.post<{
      access_token: string;
      token_type: string;
      organization: Organization;
    }>('/auth/register', data);
    return response.data;
  },

  login: async (access_code: string, password: string) => {
    const response = await api.post<{
      access_token: string;
      token_type: string;
      organization: Organization;
    }>('/auth/login', { access_code, password });
    return response.data;
  },

  getMe: async () => {
    const response = await api.get<Organization>('/auth/me');
    return response.data;
  },

  googleLogin: async (credential: string) => {
    const response = await api.post<{
      access_token: string;
      token_type: string;
      organization: Organization;
    }>('/auth/google', { credential });
    return response.data;
  },
};

export const questionsApi = {
  getQuestions: async () => {
    const response = await api.get<Question[]>('/questions/');
    return response.data;
  },

  getCategories: async () => {
    const response = await api.get<{ categories: string[] }>('/questions/categories');
    return response.data.categories;
  },
};

export const assessmentsApi = {
  create: async (level: number = 1) => {
    const response = await api.post<Assessment>(`/assessments/?level=${level}`, {});
    return response.data;
  },

  getAll: async () => {
    const response = await api.get<Assessment[]>('/assessments/');
    return response.data;
  },

  getById: async (id: number) => {
    const response = await api.get<Assessment>(`/assessments/${id}`);
    return response.data;
  },

  submit: async (assessmentId: number, answers: Answer[]) => {
    const response = await api.post<Assessment>(`/assessments/${assessmentId}/submit`, { answers });
    return response.data;
  },
  saveProgress: async (assessmentId: number, answers: Answer[]) => {
    const response = await api.put(`/assessments/${assessmentId}/save-progress`, { answers });
    return response.data;
  },

  getReport: async (id: number) => {
    const response = await api.get<{
      report: string;
      scores: Record<string, number>;
      maturity_level: number;
      gap_analysis: Record<string, any>;
    }>(`/assessments/${id}/report`);
    return response.data;
  },
};

export const assistantApi = {
  chat: async (data: {
    question_text: string;
    question_hint: string;
    options: string[];
    user_message: string;
    organization_type: string;
    organization_sector: string;
  }) => {
    const response = await api.post<{ response: string }>('/assistant/chat', data);
    return response.data;
  },
};

export const organizationApi = {
  update: async (data: {
    fiscal_code?: string;
    phone?: string;
    admin_name?: string;
    sector?: string;
    size?: string;
  }) => {
    const response = await api.put<Organization>('/auth/organization', data);
    return response.data;
  },
};

export const questionsLevel2Api = {
  getQuestions: async () => {
    const response = await api.get<{
      questions: Level2Question[];
      categories: string[];
      total: number;
    }>('/questions-level2/');
    return response.data;
  },
  
  checkEligibility: async () => {
    const response = await api.get<{
      eligible: boolean;
      completed_level1_count: number;
      message: string;
    }>('/questions-level2/check-eligibility');
    return response.data;
  },
};

export default api;
