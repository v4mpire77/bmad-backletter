export interface Document {
  id: string; // UUID
  org_id: string;
  filename: string;
  mime_type: string;
  size_bytes: number;
  storage_uri: string;
  sha256: string;
  status: 'uploaded' | 'processing' | 'completed' | 'error';
  created_at: string; // ISO 8601
}

export interface Job {
  id: string; // UUID
  doc_id: string;
  status: 'queued' | 'running' | 'done' | 'error';
  error_message?: string;
  created_at: string;
}

export interface Sentence {
  id: string;
  doc_id: string;
  page_number: number;
  text: string;
  start_char: number;
  end_char: number;
}

export interface Finding {
  id: string;
  doc_id: string;
  rule_id: string; // e.g., "art28-3-a"
  verdict: 'pass' | 'weak' | 'missing' | 'needs_review';
  snippet: string; // The evidence window text
  location: {
    page: number;
    start_char: number;
    end_char: number;
  };
}
