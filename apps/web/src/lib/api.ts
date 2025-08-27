import type { JobStatusDto } from "@/lib/types";

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
  return (await res.json()) as JobStatusDto;
}

export async function getJob(jobId: string): Promise<JobStatusDto> {
  const res = await fetch(`${apiBase()}/api/jobs/${jobId}`, { cache: "no-store" });
  if (!res.ok) {
    const detail = await safeDetail(res);
    throw new Error(`job_fetch_failed:${res.status}:${detail}`);
  }
  return (await res.json()) as JobStatusDto;
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
