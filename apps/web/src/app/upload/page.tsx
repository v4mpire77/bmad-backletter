"use client";

import React, { useCallback, useState } from "react";
import UploadCard from "@/components/UploadCard";
import UploadStatusPanel from "@/components/UploadStatusPanel";
import ResultPanel from "@/components/ResultPanel";
import useJobPolling from "@/lib/useJobPolling";

export default function UploadPage() {
  const [jobId, setJobId] = useState<string | null>(null);
  const { result, error, abort } = useJobPolling(jobId ?? undefined);

  const reset = useCallback(() => {
    abort();
    setJobId(null);
  }, [abort]);

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold">Upload a contract</h1>
      <p className="text-sm text-muted-foreground">Drop a file to create a new analysis.</p>
      {!jobId && <UploadCard onJobStart={setJobId} />}
      {jobId && <UploadStatusPanel result={result} />}
      {error && (
        <div role="alert" className="rounded bg-yellow-100 p-2 text-sm text-yellow-800">
          {error.message}
        </div>
      )}
      {result?.status === "failed" && (
        <button className="rounded border px-3 py-1 text-sm" onClick={reset}>
          Retry
        </button>
      )}
      {result?.status === "done" && result.analysisId && (
        <ResultPanel analysisId={result.analysisId} onReset={reset} />
      )}
    </div>
  );
}
