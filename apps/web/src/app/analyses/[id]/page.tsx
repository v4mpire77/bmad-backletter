import AnalysisClient from "@/components/AnalysisClient";
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

async function fetchFindings(id: string): Promise<Finding[] | null> {
  if (process.env.NEXT_PUBLIC_USE_MOCKS === "1") return getMockFindings(id);
  const base =
    process.env.NEXT_PUBLIC_API_BASE ||
    process.env.NEXT_PUBLIC_API_URL ||
    "http://localhost:8000";
  try {
    const res = await fetch(`${base}/api/analyses/${id}/findings`, { cache: "no-store" });
    if (!res.ok) return null;
    return (await res.json()) as Finding[];
  } catch {
    return null;
  }
}

export default async function AnalysisPage({ params }: { params: { id: string } }) {
  const id = params.id;
  const [summary, findings] = await Promise.all([fetchSummary(id), fetchFindings(id)]);
  const findingsError = findings === null;
  const findingsSafe: Finding[] = findings ?? [];
  const summaryError = summary === null;

  return (
    <div className="mx-auto max-w-6xl p-6">
      <Suspense fallback={<div>Loading findings…</div>}>
        <AnalysisClient summary={summary} findings={findingsSafe} findingsError={findingsError} summaryError={summaryError} />
      </Suspense>
    </div>
  );
}
