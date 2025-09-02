export interface Sentence {
  text: string;
  page: number;
  start: number;
  end: number;
}

export interface Document {
  id: string;
  filename: string;
}

export interface Job {
  id: string;
  status: 'queued' | 'running' | 'done' | 'error';
  analysis_id?: string;
  error_reason?: string | null;
  created_at?: string;
}

export interface Finding {
  detector_id: string;
  rule_id: string;
  verdict: 'pass' | 'weak' | 'missing' | 'needs_review';
  snippet: string;
  page: number;
  start: number;
  end: number;
  rationale: string;
  category?: string;
  confidence?: number;
  reviewed: boolean;
}
