import VerdictChips from "@/components/VerdictChips";
import FindingsClient from "@/components/FindingsClient";
import ExportClient from "@/components/ExportClient";
import { getMockAnalysisSummary, getMockFindings } from "@/lib/mocks";
import type { AnalysisSummary, Finding } from "@/lib/types";
import { Suspense } from "react";

async function fetchSummary(id: string): Promise<AnalysisSummary | null> {
  if (process.env.NEXT_PUBLIC_USE_MOCKS === "1") return getMockAnalysisSummary(id);
  const base =
    process.env.NEXT_PUBLIC_API_BASE ||
    process.env.NEXT_PUBLIC_API_URL ||
    "http://localhost:8000";
  try {
    const res = await fetch(`${base}/api/analyses/${id}`, { cache: "no-store" });
    if (!res.ok) return null;
    return (await res.json()) as AnalysisSummary;
  } catch {
    return null;
  }
}

async function fetchFindings(id: string): Promise<Finding[]> {
  if (process.env.NEXT_PUBLIC_USE_MOCKS === "1") return getMockFindings(id);
  const base =
    process.env.NEXT_PUBLIC_API_BASE ||
    process.env.NEXT_PUBLIC_API_URL ||
    "http://localhost:8000";
  try {
    const res = await fetch(`${base}/api/analyses/${id}/findings`, { cache: "no-store" });
    if (!res.ok) return [];
    return (await res.json()) as Finding[];
  } catch {
    return [];
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
