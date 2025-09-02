'use client';

import { useState } from 'react';
import type { PageFinding } from '@/lib/types';
import { toFinding } from '@/lib/types';
import FindingsTable from '@/components/FindingsTable';
import EvidenceDrawer from '@/components/EvidenceDrawer';
import { mockAnalysis } from '@/lib/mockReports';

export default function AnalysesClient({ id }: { id: string }) {
  const [selected, setSelected] = useState<PageFinding | null>(null);

  const analysis = mockAnalysis; // TODO: fetch by id

  const onRowClick = (f: PageFinding) => setSelected(f);
  const onClose = () => setSelected(null);

  if (!analysis) return <div>Loading analysis for ID: {id}...</div>;

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-4">Analysis Findings for ID: {id}</h1>
      <FindingsTable findings={analysis.findings as PageFinding[]} onRowClick={onRowClick} />
      <EvidenceDrawer isOpen={!!selected} onClose={onClose} finding={selected ? toFinding(selected) : null} />
    </div>
  );
}
