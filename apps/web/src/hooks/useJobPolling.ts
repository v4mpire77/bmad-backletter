'use client';
import { useCallback, useEffect, useRef, useState } from 'react';

interface Options {
  jobId: string | null;
  onDone: (jobId: string) => void;
  onStatus?: (state: string) => void;
}

export function useJobPolling({ jobId, onDone, onStatus }: Options) {
  const [attempts, setAttempts] = useState(0);
  const [isStale, setIsStale] = useState(false);
  const intervalRef = useRef<NodeJS.Timeout | null>(null);
  const startRef = useRef<number | null>(null);
  const maxAttempts = Number(process.env.NEXT_PUBLIC_POLL_MAX_ATTEMPTS || 20);
  const staleMs = Number(process.env.NEXT_PUBLIC_POLL_STALE_MS || 45000);

  const start = useCallback(() => {
    if (!jobId) return;
    startRef.current = Date.now();
    intervalRef.current = setInterval(async () => {
      setAttempts((a) => a + 1);
      const res = await fetch(`/api/jobs/${jobId}`);
      let data: any = null;
      if (res.ok) {
        data = await res.json();
        onStatus?.(data.status);
        if (data.status === 'done') {
          if (intervalRef.current) clearInterval(intervalRef.current);
          onDone(jobId);
          return;
        }
      }
      const elapsed = Date.now() - (startRef.current || 0);
      if (attempts + 1 >= maxAttempts || elapsed >= staleMs) {
        setIsStale(true);
        if (intervalRef.current) clearInterval(intervalRef.current);
        const payload = {
          job_id: jobId,
          poll_attempt: attempts + 1,
          last_state: data?.status ?? 'unknown',
          elapsed_ms: elapsed,
        };
        console.log('stale_job', payload);
        if (process.env.NEXT_PUBLIC_ENABLE_TELEMETRY === 'true') {
          fetch('/telemetry', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
          });
        }
      }
    }, 1000);
  }, [jobId, onDone, attempts, maxAttempts, staleMs]);

  const retry = useCallback(() => {
    setAttempts(0);
    setIsStale(false);
    start();
  }, [start]);

  const cancel = useCallback(() => {
    if (intervalRef.current) clearInterval(intervalRef.current);
  }, []);

  useEffect(() => {
    if (jobId) {
      start();
    }
    return () => {
      if (intervalRef.current) clearInterval(intervalRef.current);
    };
  }, [jobId, start]);

  return { attempts, isStale, retry, cancel };
}
