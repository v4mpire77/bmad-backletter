# Plan — Implement 1.4 + Fix Upload Endpoint + Branch Triage

Repo assumptions: Next.js 14 (apps/web), FastAPI (apps/api). Windows-first.

---

## Scope

* Fix upload endpoint mismatch to `POST /api/contracts`.
* Implement Story **1.4 — Display Analysis Findings UI**:

  * Findings table with verdict chips.
  * Evidence drawer (±2 sentences) wired to API.
  * Skeleton loader while fetching.
* Wire `/analyses/[id]` to real API.
* Prepare hooks and util types.
* Optional: connect Export dialog to `/api/reports/{jobId}`.
* Branch triage and merge strategy.

---

## Tasks

1. **Upload endpoint**

* File: `apps/web/src/components/UploadDropzone.tsx`
* Change target from legacy `/api/upload` to `/api/contracts`.

2. **Routing**

* Ensure there is a page: `apps/web/src/app/analyses/[id]/page.tsx` (App Router) or `pages/analyses/[id].tsx` (Pages Router). Implementation below uses **App Router**.

3. **Hooks**

* Add `useAnalysis.ts` and `useFindings.ts` under `apps/web/src/hooks/`.

4. **UI**

* Add `VerdictChip.tsx`, `SkeletonLoader.tsx`, `EvidenceDrawer.tsx`, `FindingsTable.tsx` in `apps/web/src/components/findings/`.

5. **Export** (optional now)

* Wire `ExportDialog.tsx` to call `/api/reports/{jobId}` and `/api/reports/{jobId}.pdf`.

6. **Branch triage**

* Create local tracking branches and preview diffs. Prefer low-divergence branches.

---

## Code Changes — Web

### 1) Upload endpoint

```diff
--- a/apps/web/src/components/UploadDropzone.tsx
+++ b/apps/web/src/components/UploadDropzone.tsx
@@
- const endpoint = process.env.NEXT_PUBLIC_API_URL + "/api/upload";
+ const endpoint = (process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000") + "/api/contracts";
@@
- const res = await fetch(endpoint, { method: "POST", body: formData });
+ const res = await fetch(endpoint, { method: "POST", body: formData }); // FastAPI expects `file` field
```

If field name is wrong:

```diff
- formData.append("document", file)
+ formData.append("file", file)
```

### 2) Hooks

**`apps/web/src/hooks/useAnalysis.ts`**

```ts
import { useEffect, useState } from "react";

export type JobStatus = "queued" | "processing" | "complete" | "failed";
export interface JobStatusResponse { job_id: string; status: JobStatus; error?: string | null; findings_count: number }

export function useAnalysis(jobId: string) {
  const [data, setData] = useState<JobStatusResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const base = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

  useEffect(() => {
    let timer: NodeJS.Timeout;
    async function tick() {
      try {
        const r = await fetch(`${base}/api/jobs/${jobId}`);
        if (!r.ok) throw new Error(await r.text());
        const j: JobStatusResponse = await r.json();
        setData(j);
        if (j.status !== "complete" && j.status !== "failed") {
          timer = setTimeout(tick, 1500);
        } else {
          setLoading(false);
        }
      } catch (e: any) {
        setError(e.message);
        setLoading(false);
      }
    }
    tick();
    return () => { if (timer) clearTimeout(timer); };
  }, [jobId, base]);

  return { data, loading, error };
}
```

**`apps/web/src/hooks/useFindings.ts`**

```ts
import { useEffect, useState } from "react";

export type Verdict = "Pass" | "Weak" | "Missing" | "Needs Review";
export interface Finding { rule_id: string; rule_name: string; verdict: Verdict; snippet: string; page?: number | null; rationale?: string | null }
export interface FindingsResponse { job_id: string; findings: Finding[]; rulepack_version?: string | null }

export function useFindings(jobId: string, enabled: boolean) {
  const [data, setData] = useState<FindingsResponse | null>(null);
  const [loading, setLoading] = useState(enabled);
  const [error, setError] = useState<string | null>(null);
  const base = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

  useEffect(() => {
    if (!enabled) return;
    let cancelled = false;
    async function run() {
      try {
        const r = await fetch(`${base}/api/findings?job_id=${encodeURIComponent(jobId)}`);
        if (!r.ok) throw new Error(await r.text());
        const j: FindingsResponse = await r.json();
        if (!cancelled) setData(j);
      } catch (e: any) {
        if (!cancelled) setError(e.message);
      } finally {
        if (!cancelled) setLoading(false);
      }
    }
    run();
    return () => { cancelled = true; };
  }, [jobId, base, enabled]);

  return { data, loading, error };
}
```

### 3) Components

**`apps/web/src/components/findings/VerdictChip.tsx`**

```tsx
export function VerdictChip({ verdict }: { verdict: "Pass"|"Weak"|"Missing"|"Needs Review" }) {
  const cls = verdict === "Pass" ? "bg-green-100 text-green-800" : verdict === "Weak" ? "bg-amber-100 text-amber-800" : verdict === "Missing" ? "bg-red-100 text-red-800" : "bg-blue-100 text-blue-800";
  return <span className={`px-2 py-0.5 rounded text-xs font-medium ${cls}`}>{verdict}</span>;
}
```

**`apps/web/src/components/findings/SkeletonLoader.tsx`**

```tsx
export function SkeletonLoader() {
  return (
    <div className="space-y-3">
      {[...Array(6)].map((_, i) => (
        <div key={i} className="h-6 bg-gray-200/70 animate-pulse rounded" />
      ))}
    </div>
  );
}
```

**`apps/web/src/components/findings/EvidenceDrawer.tsx`**

```tsx
import { useState } from "react";
import { Finding } from "@/hooks/useFindings";

export function EvidenceDrawer({ finding, onClose }: { finding: Finding|null; onClose: ()=>void }) {
  return (
    <div className={`fixed inset-0 ${finding ? "pointer-events-auto" : "pointer-events-none"}`}>
      <div className={`absolute inset-0 bg-black/30 ${finding ? "opacity-100" : "opacity-0"}`} onClick={onClose} />
      <aside className={`absolute right-0 top-0 h-full w-full max-w-xl bg-white shadow-xl p-4 transition-transform ${finding ? "translate-x-0" : "translate-x-full"}`}>
        {finding && (
          <div className="space-y-3">
            <h2 className="text-lg font-semibold">{finding.rule_name} <span className="text-gray-500 text-sm">({finding.rule_id})</span></h2>
            <p className="text-sm text-gray-800 whitespace-pre-wrap">{finding.snippet}</p>
            {finding.rationale && <p className="text-xs text-gray-500">Rationale: {finding.rationale}</p>}
          </div>
        )}
      </aside>
    </div>
  );
}
```

**`apps/web/src/components/findings/FindingsTable.tsx`**

```tsx
import { useState } from "react";
import { FindingsResponse, Finding } from "@/hooks/useFindings";
import { VerdictChip } from "./VerdictChip";
import { EvidenceDrawer } from "./EvidenceDrawer";

export function FindingsTable({ data }: { data: FindingsResponse }) {
  const [selected, setSelected] = useState<Finding|null>(null);
  const [filter, setFilter] = useState<string>("all");
  const rows = data.findings.filter(f => filter === "all" ? true : f.verdict === filter);
  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <label className="text-sm">Filter:</label>
        <select className="border rounded px-2 py-1 text-sm" value={filter} onChange={e=>setFilter(e.target.value)}>
          {(["all","Pass","Weak","Missing","Needs Review"] as const).map(v => <option key={v} value={v}>{v}</option>)}
        </select>
      </div>
      <table className="w-full text-sm">
        <thead>
          <tr className="text-left text-gray-600">
            <th className="py-2">Obligation</th>
            <th className="py-2">Verdict</th>
            <th className="py-2">Snippet</th>
          </tr>
        </thead>
        <tbody>
          {rows.map((f, i) => (
            <tr key={`${f.rule_id}-${i}`} className="border-t hover:bg-gray-50 cursor-pointer" onClick={()=>setSelected(f)}>
              <td className="py-2 pr-3">{f.rule_name}</td>
              <td className="py-2 pr-3"><VerdictChip verdict={f.verdict} /></td>
              <td className="py-2 pr-3 text-gray-700 truncate">{f.snippet}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <EvidenceDrawer finding={selected} onClose={()=>setSelected(null)} />
    </div>
  );
}
```

### 4) Page — `/analyses/[id]`

**`apps/web/src/app/analyses/[id]/page.tsx`**

```tsx
"use client";
import { useParams } from "next/navigation";
import { useAnalysis } from "@/hooks/useAnalysis";
import { useFindings } from "@/hooks/useFindings";
import { SkeletonLoader } from "@/components/findings/SkeletonLoader";
import { FindingsTable } from "@/components/findings/FindingsTable";

export default function AnalysisDetailPage() {
  const params = useParams();
  const jobId = String(params?.id ?? "");
  const { data: job, loading: loadingJob, error: jobError } = useAnalysis(jobId);
  const { data: findings, loading: loadingFindings, error: findingsError } = useFindings(jobId, !!job && job.status === "complete");

  if (jobError) return <p className="text-red-600 text-sm">{jobError}</p>;

  return (
    <div className="max-w-5xl mx-auto p-6 space-y-6">
      <header className="flex items-center justify-between">
        <h1 className="text-xl font-semibold">Analysis {jobId}</h1>
        <div className="text-sm text-gray-600">Status: {job?.status ?? "…"}</div>
      </header>

      {loadingJob && <SkeletonLoader />}

      {job?.status === "processing" || job?.status === "queued" ? (
        <p className="text-sm text-gray-600">Processing… this page will auto-refresh.</p>
      ) : null}

      {findingsError && <p className="text-red-600 text-sm">{findingsError}</p>}

      {findings && <FindingsTable data={findings} />}

      {loadingFindings && <SkeletonLoader />}
    </div>
  );
}
```

### 5) Optional — Export

**`apps/web/src/components/ExportDialog.tsx`**

```tsx
export async function exportReport(jobId: string, fmt: "html"|"pdf") {
  const base = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";
  const url = fmt === "pdf" ? `${base}/api/reports/${jobId}.pdf` : `${base}/api/reports/${jobId}`;
  const r = await fetch(url);
  if (!r.ok) throw new Error(await r.text());
  if (fmt === "pdf") {
    const blob = await r.blob();
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `blackletter-${jobId}.pdf`;
    a.click();
  } else {
    const html = await r.text();
    const blob = new Blob([html], { type: "text/html" });
    const a = document.createElement("a");
    a.href = URL.createObjectURL(blob);
    a.download = `blackletter-${jobId}.html`;
    a.click();
  }
}
```

---

## Navigation links

* Ensure analyses list links to `/analyses/[id]` (from Dashboard History 3.3).
* Add table column with link using Next `<Link href={`/analyses/${row.job_id}`}>Open</Link>`.

---

## Tests

* **Vitest**: unit test `VerdictChip`, `FindingsTable` filter logic.
* **Integration**: mock fetch for `/api/jobs/:id` and `/api/findings?job_id=...`.
* **E2E (Playwright)**: upload → wait → verify table renders 8 rows.

Minimal examples:

```ts
// apps/web/src/components/findings/__tests__/verdictChip.test.tsx
// render component for each verdict and assert classes exist
```

---

## Branch Triage & Merge Plan

### Low-divergence candidates first

* `origin/copilot/fix-f23696e4-ec15-4e56-afa1-aa17d6bfb0f6` — 4 ahead / 15 behind
* `origin/copilot/fix-edd60661-99f0-4b6b-af62-4cf428e17dfb` — 6 ahead / 33 behind
* `origin/codex/fix-pytest-for-all-python-versions` — 1 ahead / 10 behind
* `origin/codex/add-bmad-scripts-to-package.json` — 1 ahead / 33 behind

### Preview diffs (Windows PowerShell)

```powershell
# Create local tracking branch and view diff summary
$branches = @(
  "origin/copilot/fix-f23696e4-ec15-4e56-afa1-aa17d6bfb0f6",
  "origin/copilot/fix-edd60661-99f0-4b6b-af62-4cf428e17dfb",
  "origin/codex/fix-pytest-for-all-python-versions"
)
foreach ($rb in $branches) {
  $name = $rb -replace '^origin/', ''
  git fetch origin $name
  git branch -f preview/$name $rb
  git --no-pager diff --stat main..preview/$name | Write-Host
}
```

### Conflict forecast

```powershell
# Names only to gauge surface area
git --no-pager diff --name-only main..preview/copilot/fix-f23696e4-ec15-4e56-afa1-aa17d6bfb0f6
```

### Merge strategy

1. Rebase preview branches onto `main` locally, fix conflicts, run tests.
2. If scope is clean, fast-forward merge. Otherwise cherry-pick specific commits.
3. Defer high-divergence branches (behind > 100) unless a must-have patch exists.

---

## Done Criteria

* Upload uses `/api/contracts` and succeeds.
* `/analyses/[id]` shows status, auto-polls, and renders findings with chips + drawer.
* Skeletons display during pending states.
* Dashboard history links open detail page.
* Optional export works.
* CI green on Windows.

---

## Next

* 4.2 Coverage Meter component on findings header.
* 5.1 Org Settings scaffold (feature flag only UI stub).
* 6.1 Compliance Modes doc + API schema draft.

