import { useEffect, useState } from 'react';
import type { Finding } from '@/types';

interface JobResponse {
  status: 'queued' | 'running' | 'done' | 'error';
  error?: string;
}

export default function useJobStatus(id: string) {
  const [status, setStatus] = useState<JobResponse['status']>('queued');
  const [findings, setFindings] = useState<Finding[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    let timer: NodeJS.Timeout;

    const poll = async () => {
      try {
        const res = await fetch(`/api/jobs/${id}`);
        if (!res.ok) throw new Error('status_failed');
        const data: JobResponse = await res.json();
        if (cancelled) return;
        setStatus(data.status);
        if (data.status === 'done') {
          const fRes = await fetch(`/api/analyses/${id}`);
          if (!fRes.ok) throw new Error('findings_failed');
          const fData = await fRes.json();
          if (cancelled) return;
          setFindings(fData.findings || fData);
        } else if (data.status === 'queued' || data.status === 'running') {
          timer = setTimeout(poll, 1000);
        }
      } catch {
        if (!cancelled) setError('Failed to load job status.');
      }
    };

    poll();
    return () => {
      cancelled = true;
      if (timer) clearTimeout(timer);
    };
  }, [id]);

  return { status, findings, error };
}
