import type { JobStatusDto, AnalysisSummary, Finding } from "@/lib/types";

function apiBase(): string {
  return (
    process.env.NEXT_PUBLIC_API_BASE ||
    process.env.NEXT_PUBLIC_API_URL ||
    "http://localhost:8000"
  );
}

export async function uploadContract(file: File): Promise<JobStatusDto> {
  const fd = new FormData();
  fd.append("file", file, file.name);
  const res = await fetch(`${apiBase()}/api/contracts`, {
    method: "POST",
    body: fd,
  });
  if (!res.ok) {
    const detail = await safeDetail(res);
    throw new Error(`upload_failed:${res.status}:${detail}`);
  }
  const data = await res.json();
  return {
    id: data.id,
    status: data.status,
    analysis_id: data.analysis_id,
    error_reason: data.error_reason,
    created_at: data.created_at,
  } as JobStatusDto;
}

export async function getJob(jobId: string): Promise<JobStatusDto> {
  const res = await fetch(`${apiBase()}/api/jobs/${jobId}`, { cache: "no-store" });
  if (!res.ok) {
    const detail = await safeDetail(res);
    throw new Error(`job_fetch_failed:${res.status}:${detail}`);
  }
  const data = await res.json();
  return {
    id: data.id,
    status: data.status,
    analysis_id: data.analysis_id,
    error_reason: data.error_reason,
    created_at: data.created_at,
  } as JobStatusDto;
}

export async function getAnalyses(limit = 50): Promise<AnalysisSummary[]> {
  const res = await fetch(`${apiBase()}/api/analyses?limit=${limit}`, {
    cache: "no-store"
  });
  if (!res.ok) {
    const detail = await safeDetail(res);
    throw new Error(`analyses_fetch_failed:${res.status}:${detail}`);
  }
  const data = await res.json();
  return data.map((item: any) => ({
    id: item.id,
    filename: item.filename,
    created_at: item.created_at,
    size: item.size,
    state: item.state,
    verdicts: item.verdicts,
  })) as AnalysisSummary[];
}

export async function getAnalysis(analysisId: string): Promise<AnalysisSummary> {
  const res = await fetch(`${apiBase()}/api/analyses/${analysisId}`, {
    cache: "no-store"
  });
  if (!res.ok) {
    const detail = await safeDetail(res);
    throw new Error(`analysis_fetch_failed:${res.status}:${detail}`);
  }
  const data = await res.json();
  return {
    id: data.id,
    filename: data.filename,
    created_at: data.created_at,
    size: data.size,
    state: data.state,
    verdicts: data.verdicts,
  } as AnalysisSummary;
}

export async function getFindings(analysisId: string): Promise<Finding[]> {
  const res = await fetch(`${apiBase()}/api/analyses/${analysisId}/findings`, {
    cache: "no-store"
  });
  if (!res.ok) {
    const detail = await safeDetail(res);
    throw new Error(`findings_fetch_failed:${res.status}:${detail}`);
  }
  const data = await res.json();
  return data.map((item: any) => ({
    detector_id: item.detector_id,
    rule_id: item.rule_id,
    verdict: item.verdict,
    snippet: item.snippet,
    page: item.page,
    start: item.start,
    end: item.end,
    rationale: item.rationale,
    reviewed: item.reviewed || false,
  })) as Finding[];
}

async function safeDetail(res: Response): Promise<string> {
  try {
    const data: unknown = await res.json();
    const detail = (data as { detail?: unknown })?.detail;
    return typeof detail === "string" ? detail : String(res.statusText);
  } catch {
    return res.statusText;
  }
}
