import axios from 'axios';
import { Organization, Question, Assessment, Answer } from './types';

const API_BASE = import.meta.env.VITE_API_URL || '/api';

const api = axios.create({
  baseURL: API_BASE,
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
  create: async () => {
    const response = await api.post<Assessment>('/assessments/');
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

  submit: async (id: number, answers: Answer[]) => {
    const response = await api.post<Assessment>(`/assessments/${id}/submit`, {
      answers,
    });
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

export default api;
