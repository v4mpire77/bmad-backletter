// Canonical domain types for Evidence & Findings UI

export type Anchor = {
  text: string;
  page: number;
  offset: number;
};

export type Citation = {
  page: number;
  text: string;
  start?: number;
  end?: number;
};

export type Finding = {
  id: string;
  title: string;
  verdict: 'ok' | 'weak' | 'missing';
  evidence: string;
  rationale?: string;
  anchors: Anchor[];
  citations?: Citation[];
};

// Legacy page finding used by tables/pages
export type PageFinding = {
  id?: string;
  rule_id: string;
  snippet: string;
  evidence?: Array<{ page: number; start: number; end: number }>;
  anchors?: string[];
};

export function ensurePageFindingIds(
  findings: PageFinding[],
): Array<PageFinding & { id: string }> {
  return findings.map((f) => ({ ...f, id: f.id ?? crypto.randomUUID() }));
}

// Adapter: PageFinding -> Finding (for Drawer)
export function toFinding(f: PageFinding): Finding {
  const evidenceText = f.snippet;
  const anchors: Anchor[] = (f.anchors ?? [])
    .map((text) => {
      const offset = evidenceText.toLowerCase().indexOf(text.toLowerCase());
      if (offset === -1) return null;
      return { text, page: f.evidence?.[0]?.page ?? 1, offset };
    })
    .filter(Boolean) as Anchor[];

  const citations: Citation[] = (f.evidence ?? []).map((ev) => ({
    page: ev.page,
    text: evidenceText,
    start: ev.start,
    end: ev.end,
  }));

  return {
    id: f.id ?? crypto.randomUUID(),
    title: f.rule_id,
    verdict: 'weak',
    evidence: evidenceText,
    anchors,
    citations,
  };
}

