'use client';
import { useState } from 'react';
import { useSearchParams } from 'next/navigation';
import type { PageFinding } from '@/lib/types';
import { toFinding } from '@/lib/types';
import FindingsTable from '@/components/FindingsTable';
import EvidenceDrawer from '@/components/EvidenceDrawer';
import { mockAnalysis } from '@/lib/mockReports';

export default function AnalysesPage() {
  const [selected, setSelected] = useState<PageFinding | null>(null);
  const searchParams = useSearchParams();
  const jobId = searchParams.get('jobId') || 'mock-job-123';

  const analysis = mockAnalysis; // TODO: fetch by jobId

  const onRowClick = (f: PageFinding) => setSelected(f);
  const onClose = () => setSelected(null);

  if (!analysis) return <div>Loading analysis for job ID: {jobId}...</div>;

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-4">Analysis Findings for Job ID: {jobId}</h1>
      <FindingsTable findings={analysis.findings as PageFinding[]} onRowClick={onRowClick} />
      <EvidenceDrawer isOpen={!!selected} onClose={onClose} finding={selected ? toFinding(selected) : null} />
    </div>
  );
}
