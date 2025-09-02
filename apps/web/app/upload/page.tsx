"use client";

import { useState } from "react";
import { createJob, pollJobUntilDone } from "@/lib/api";
import { useRouter } from "next/navigation";

export default function UploadPage() {
  const [file, setFile] = useState<File | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const router = useRouter();

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    if (!file) return setError("Choose a PDF or DOCX file.");

    try {
      setBusy(true);
      const { job_id } = await createJob(file);
      await pollJobUntilDone(job_id, 60000); // wait up to 60s; adjust as needed
      router.push(`/analyses/${job_id}`);
    } catch (err: any) {
      setError(err?.message ?? "Upload failed");
    } finally {
      setBusy(false);
    }
  };

  return (
    <section className="space-y-6">
      <h1 className="text-2xl font-semibold">Upload a Contract</h1>

      <form onSubmit={onSubmit} className="rounded-xl border bg-white p-6 space-y-4">
        <input
          type="file"
          accept=".pdf,.docx,application/pdf,application/vnd.openxmlformats-officedocument.wordprocessingml.document"
          onChange={(e) => setFile(e.target.files?.[0] ?? null)}
        />
        <button
          disabled={!file || busy}
          className="rounded-lg px-4 py-2 border bg-black text-white disabled:opacity-50"
        >
          {busy ? "Uploading…" : "Start Analysis"}
        </button>
        {error && <p className="text-red-600 text-sm">{error}</p>}
        <p className="text-xs text-neutral-500">
          Max 10MB. Supported: PDF, DOCX. You’ll be taken to the findings when ready.
        </p>
      </form>
    </section>
  );
}
