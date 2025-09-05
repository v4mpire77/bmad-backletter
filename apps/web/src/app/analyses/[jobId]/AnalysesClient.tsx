'use client';

import { useMemo, useState } from 'react';
import type { PageFinding } from '@/lib/types';
import { toFinding, ensurePageFindingIds } from '@/lib/types';
import FindingsTable from '@/components/FindingsTable';
import EvidenceDrawer from '@/components/EvidenceDrawer';
import { mockAnalysis } from '@/lib/mockReports';

export default function AnalysesClient({ jobId }: { jobId: string }) {
  const [selected, setSelected] = useState<PageFinding | null>(null);

  const analysis = mockAnalysis; // TODO: fetch by jobId
  const findings = useMemo(
    () => ensurePageFindingIds(analysis.findings as PageFinding[]),
    [analysis.findings],
  );

  const onRowClick = (f: PageFinding) => setSelected(f);
  const onClose = () => setSelected(null);

  if (!analysis) return <div>Loading analysis for job ID: {jobId}...</div>;

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-4">Analysis Findings for Job ID: {jobId}</h1>
      <FindingsTable findings={findings} onRowClick={onRowClick} />
      <EvidenceDrawer isOpen={!!selected} onClose={onClose} finding={selected ? toFinding(selected) : null} />
    </div>
  );
}
