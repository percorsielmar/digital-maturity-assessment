export interface Organization {
  id: number;
  name: string;
  type: string;
  sector: string | null;
  size: string | null;
  email: string | null;
  fiscal_code: string | null;
  phone: string | null;
  admin_name: string | null;
  access_code: string;
  created_at: string;
}

export interface QuestionOption {
  text: string;
  score: number;
}

export interface Question {
  id: number;
  category: string;
  subcategory: string | null;
  text: string;
  hint: string | null;
  options: QuestionOption[];
  weight: number;
  order: number;
}

export interface Answer {
  question_id: number;
  selected_option: number;
  notes?: string;
}

export interface Assessment {
  id: number;
  organization_id: number;
  level: number;
  status: string;
  scores: Record<string, number>;
  maturity_level: number | null;
  gap_analysis: Record<string, GapAnalysisItem>;
  report: string | null;
  responses?: {
    answers: Array<{
      question_id: number;
      selected_option: number;
      notes?: string;
    }>;
  };
  created_at: string;
  completed_at: string | null;
}

export interface Level2Question {
  id: number;
  category: string;
  subcategory: string;
  code: string;
  text: string;
  type: 'text' | 'select' | 'multiselect';
  required: boolean;
  options: Array<{ value: string; text: string; score?: number }> | null;
  hint: string;
  conditional?: { question_id: number; value: string };
}

export interface GapAnalysisItem {
  current_score: number;
  target_score: number;
  gap: number;
  priority: string;
}

export interface AuthState {
  token: string | null;
  organization: Organization | null;
  isAuthenticated: boolean;
}
