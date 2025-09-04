import { useEffect, useMemo, useState } from "react";

export type Verdict = "pass" | "weak" | "missing" | "needs_review";

export interface Finding {
  detector_id: string;
  rule_id: string;
  verdict: Verdict;
  snippet: string;
  page: number;
  start: number;
  end: number;
  rationale: string;
  category?: string | null;
  confidence?: number | null;
  reviewed?: boolean;
  weak_language_detected?: boolean;
  lexicon_version?: string | null;
}

export function useFindings(analysisId: string) {
  const [data, setData] = useState<Finding[] | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!analysisId) return;
    let cancelled = false;
    const base = (process.env.NEXT_PUBLIC_API_URL ?? "").replace(/\/$/, "");

    async function run() {
      try {
        setLoading(true);
        const res = await fetch(`${base}/api/analyses/${analysisId}/findings`);
        if (!res.ok) throw new Error(await res.text());
        const json = (await res.json()) as Finding[];
        if (!cancelled) setData(json);
      } catch (e: any) {
        if (!cancelled) setError(e.message || "Failed to load findings");
      } finally {
        if (!cancelled) setLoading(false);
      }
    }

    run();
    return () => {
      cancelled = true;
    };
  }, [analysisId]);

  const verdictCounts = useMemo(() => {
    const counts = { pass: 0, weak: 0, missing: 0, needs_review: 0 } as Record<Verdict, number>;
    (data ?? []).forEach((f) => (counts[f.verdict] += 1));
    return counts;
  }, [data]);

  return { data, loading, error, verdictCounts };
}

