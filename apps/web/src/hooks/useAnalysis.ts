import { useEffect, useState } from "react";

export interface VerdictCounts {
  pass_count: number;
  weak_count: number;
  missing_count: number;
  needs_review_count: number;
}

export interface AnalysisSummary {
  id: string;
  filename: string;
  created_at: string;
  size: number;
  state: string;
  verdicts: VerdictCounts;
}

export function useAnalysis(analysisId: string) {
  const [data, setData] = useState<AnalysisSummary | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!analysisId) return;
    let cancelled = false;
    const base = (process.env.NEXT_PUBLIC_API_URL ?? "").replace(/\/$/, "");

    async function run() {
      try {
        setLoading(true);
        const res = await fetch(`${base}/api/analyses/${analysisId}`);
        if (!res.ok) throw new Error(await res.text());
        const json = (await res.json()) as AnalysisSummary;
        if (!cancelled) setData(json);
      } catch (e: any) {
        if (!cancelled) setError(e.message || "Failed to load analysis");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    run();
    return () => {
      cancelled = true;
    };
  }, [analysisId]);

  return { data, loading, error };
}

