"use client";
import { useAnalysis } from '@/hooks/useAnalysis';
import { useFindings } from '@/hooks/useFindings';
import SkeletonLoader from '@/components/findings/SkeletonLoader';
import FindingsTable from '@/components/findings/FindingsTable';

interface AnalysisDetailClientProps {
  jobId: string;
}

export default function AnalysisDetailClient({ jobId }: AnalysisDetailClientProps) {
  const { data: analysis, loading: loadingAnalysis, error: analysisError } = useAnalysis(jobId);
  const { data: findings, loading: loadingFindings, error: findingsError } = useFindings(jobId);

  if (!jobId) {
    return <p className="text-sm text-red-600">Invalid analysis id</p>;
  }

  return (
    <div className="max-w-5xl mx-auto p-6 space-y-6">
      <header className="flex items-center justify-between">
        <h1 className="text-xl font-semibold">Analysis {jobId}</h1>
        <div className="text-sm text-gray-600">State: {analysis?.state ?? '…'}</div>
      </header>

      {(loadingAnalysis || (!analysis && !analysisError)) && <SkeletonLoader />}
      {analysisError && <p className="text-sm text-red-600">{analysisError}</p>}

      {findingsError && <p className="text-sm text-red-600">{findingsError}</p>}
      {findings && findings.length > 0 && <FindingsTable findings={findings} />}
      {loadingFindings && <SkeletonLoader />}
      {findings && findings.length === 0 && (
        <p className="text-sm text-gray-600">No findings available for this analysis.</p>
      )}
    </div>
  );
}

