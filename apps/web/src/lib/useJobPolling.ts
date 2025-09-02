import { useCallback, useEffect, useRef, useState } from "react";

export type JobState = "queued" | "processing" | "done" | "failed";

export interface JobPollingResult {
  status: JobState;
  analysisId?: string;
  progress?: number;
  eta?: number;
}

const mapStatus = (status?: string): JobState => {
  if (status === "running" || status === "processing") return "processing";
  if (status === "done") return "done";
  if (status === "error" || status === "failed") return "failed";
  return "queued";
};

export function useJobPolling(jobId?: string) {
  const [result, setResult] = useState<JobPollingResult | null>(null);
  const [error, setError] = useState<Error | null>(null);
  const attemptsRef = useRef(0);
  const timeoutRef = useRef<NodeJS.Timeout | null>(null);
  const abortRef = useRef<AbortController | null>(null);

  const abort = useCallback(() => {
    abortRef.current?.abort();
    if (timeoutRef.current) clearTimeout(timeoutRef.current);
  }, []);

  const poll = useCallback(async () => {
    if (!jobId) return;
    try {
      abortRef.current?.abort();
      const controller = new AbortController();
      abortRef.current = controller;
      const res = await fetch(`/api/jobs/${jobId}`, {
        signal: controller.signal,
      });
      if (!res.ok) throw new Error(`HTTP ${res.status}`);
      const data = await res.json();
      const mapped = mapStatus(data.status);
      setResult({
        status: mapped,
        analysisId: data.analysis_id,
        progress: data.progress,
        eta: data.eta,
      });
      setError(null);
      attemptsRef.current = 0;
      if (mapped === "queued" || mapped === "processing") {
        timeoutRef.current = setTimeout(poll, 2000);
      }
    } catch (err) {
      setError(err as Error);
      attemptsRef.current += 1;
      const delay =
        attemptsRef.current <= 3
          ? 2000
          : 2000 * Math.pow(2, attemptsRef.current - 3);
      timeoutRef.current = setTimeout(poll, delay);
    }
  }, [jobId]);

  useEffect(() => {
    if (!jobId) return;
    poll();
    return () => abort();
  }, [jobId, poll, abort]);

  return { result, error, abort };
}

export default useJobPolling;
