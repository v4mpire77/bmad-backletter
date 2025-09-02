// Define the structure of a finding

export interface Anchor {
  text: string;
  page: number;
  offset: number;
}

export interface Finding {
  id: string;
  detector: string;
  verdict: string; // 'pass' | 'weak' | 'missing' | 'needs_review'
  rationale: string;
  evidence: string;
  anchors: Anchor[];
  reviewed: boolean;
}