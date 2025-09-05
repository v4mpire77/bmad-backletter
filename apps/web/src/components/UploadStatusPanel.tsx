import React from "react";
import { JobPollingResult } from "@/lib/useJobPolling";

interface Props {
  result: JobPollingResult | null;
}

export default function UploadStatusPanel({ result }: Props) {
  if (!result) return null;
  const { status, progress } = result;
  return (
    <div className="mt-4" aria-live="polite">
      <p className="text-sm font-medium">Status: {status}</p>
      {status !== "done" && (
        <div role="progressbar" className="mt-2 h-2 w-full rounded bg-gray-200">
          {typeof progress === "number" ? (
            <div
              className="h-2 rounded bg-blue-500 transition-all"
              style={{ width: `${progress}%` }}
            />
          ) : (
            <div className="h-2 w-full animate-pulse rounded bg-blue-500" />
          )}
        </div>
      )}
    </div>
  );
}
