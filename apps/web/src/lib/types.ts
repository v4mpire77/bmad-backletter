// Canonical domain type used by EvidenceDrawer and cross‑component contracts
export type Finding = {
  id: string;
  rule_id: string;           // e.g. "GDPR-DSAR-001"
  snippet: string;           // evidence window text for display
  verdict?: 'pass' | 'weak' | 'missing' | 'needs_review';
  // Location of the primary evidence window (min contract for Drawer)
  location?: { page: number; start_char: number; end_char: number };
  // Optional richer traces used by highlighter or future features
  evidence?: Array<{ page: number; start: number; end: number }>;
  anchors?: string[];        // phrases to highlight inside snippet
};

// View type for tables/pages: keep minimal fields for listing
export type PageFinding = Pick<Finding, 'id' | 'rule_id' | 'snippet'> & {
  evidence?: Array<{ page: number; start: number; end: number }>;
  anchors?: string[];
};

// Adapter: PageFinding -> Finding (for Drawer)
export function toFinding(f: PageFinding): Finding {
  const first = f.evidence?.[0];
  return {
    id: f.id ?? crypto.randomUUID(),
    rule_id: f.rule_id,
    snippet: f.snippet,
    verdict: 'needs_review',
    location: first
      ? { page: first.page, start_char: first.start, end_char: first.end }
      : { page: 1, start_char: 0, end_char: Math.max(1, f.snippet.length - 1) },
    evidence: f.evidence ?? [],
    anchors: f.anchors ?? [],
  };
}