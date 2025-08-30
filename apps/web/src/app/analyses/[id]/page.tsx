import VerdictChips from "@/components/VerdictChips";
import FindingsClient from "@/components/FindingsClient";
import ExportClient from "@/components/ExportClient";
import { getAnalysis, getFindings } from "@/lib/api";
import { getMockAnalysisSummary, getMockFindings } from "@/lib/mocks";
import type { AnalysisSummary, Finding } from "@/lib/types";
import { Suspense } from "react";

async function fetchSummary(id: string): Promise<AnalysisSummary | null> {
  try {
    // Try real API first
    return await getAnalysis(id);
  } catch (error) {
    console.warn("Failed to fetch analysis from API, falling back to mocks:", error);
    // Fallback to mocks
    return getMockAnalysisSummary(id);
  }
}

async function fetchFindings(id: string): Promise<Finding[]> {
  try {
    // Try real API first
    return await getFindings(id);
  } catch (error) {
    console.warn("Failed to fetch findings from API, falling back to mocks:", error);
    // Fallback to mocks
    return getMockFindings(id);
  }
}

export default async function AnalysisPage({ params }: { params: { id: string } }) {
  const id = params.id;
  const summary = await fetchSummary(id);
  const findings = await fetchFindings(id);

  return (
    <div className="mx-auto max-w-6xl p-6">
      <header className="mb-6">
        <div className="flex items-center justify-between gap-4">
          <h1 className="text-2xl font-semibold">Findings</h1>
          <ExportClient />
        </div>
        {summary ? (
          <div className="mt-2">
            <p className="text-sm text-gray-600 dark:text-gray-300">
              {summary.filename} • {new Date(summary.created_at).toLocaleString()}
            </p>
            <div className="mt-2">
              <VerdictChips counts={summary.verdicts} />
            </div>
          </div>
        ) : (
          <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">Loading…</p>
        )}
      </header>
      <Suspense fallback={<div>Loading findings…</div>}>
        <FindingsClient initialFindings={findings} />
      </Suspense>
    </div>
  );
}
