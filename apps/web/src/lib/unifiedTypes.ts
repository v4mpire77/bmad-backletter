// Unified Finding type that consolidates all properties from different components
// This serves as the single source of truth for Finding data structures

export interface Anchor {
  text: string;
  page: number;
  offset: number;
}

export interface Finding {
  // Core identification
  id: string;
  
  // Detection and rule information
  detector: string;
  rule_id?: string; // Optional for backward compatibility
  
  // Verdict and analysis
  verdict: 'missing' | 'weak' | 'present' | 'strong' | 'pass' | 'needs_review';
  rationale: string;
  
  // Evidence and content
  evidence: string;
  snippet?: string; // Alias for evidence, for backward compatibility
  
  // Document references
  anchors: Anchor[];
  page_number?: number;
  char_start?: number;
  char_end?: number;
  context_before?: string;
  context_after?: string;
  
  // Review status
  reviewed: boolean;
}

// Analysis metadata type
export interface Analysis {
  id: string;
  status: string;
  contract_name: string;
  created_at: string;
  findings_count: number;
}

// Helper function to ensure Finding compatibility
export function ensureFindingCompleteness(finding: Partial<Finding>): Finding {
  return {
    id: finding.id || '',
    detector: finding.detector || '',
    verdict: finding.verdict || 'needs_review',
    rationale: finding.rationale || '',
    evidence: finding.evidence || finding.snippet || '',
    snippet: finding.snippet || finding.evidence || '',
    anchors: finding.anchors || [],
    reviewed: finding.reviewed || false,
    ...finding
  };
}
