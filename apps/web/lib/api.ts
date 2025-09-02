const API = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export async function createJob(file: File): Promise<{ job_id: string }> {
  const form = new FormData();
  form.append("file", file);
  const res = await fetch(`${API}/api/contracts`, { method: "POST", body: form });
  if (!res.ok) throw new Error(`Upload failed (${res.status})`);
  return res.json();
}

  if (!res.ok) throw new Error(`Job lookup failed (${res.status}): ${await res.text()}`);
  return res.json() as Promise<{ status: string; error?: string | null }>;
}

export async function pollJobUntilDone(jobId: string, timeoutMs = 60000, intervalMs = 1000) {
  const t0 = Date.now();
  while (Date.now() - t0 < timeoutMs) {
    const j = await getJob(jobId);
    if (j.status === "complete") return true;
    if (j.status === "failed") throw new Error(j.error ?? "Analysis failed");
    await new Promise((r) => setTimeout(r, intervalMs));
  }
  throw new Error("Timed out waiting for analysis");
}

  if (!res.ok) throw new Error(`Findings not ready (${res.status}): ${await res.text()}`);
  return res.json() as Promise<{
    job_id: string;
    rulepack_version?: string | null;
    findings: Array<{
      rule_id: string; rule_name: string; verdict: "Pass" | "Weak" | "Missing" | "Needs Review";
      snippet: string; page?: number | null; rationale?: string | null;
    }>;
  }>;
}
