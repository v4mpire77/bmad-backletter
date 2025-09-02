import React from "react";
import { useRouter } from "next/navigation";

interface Props {
  analysisId: string;
  onReset: () => void;
}

export default function ResultPanel({ analysisId, onReset }: Props) {
  const router = useRouter();
  return (
    <div className="mt-4 space-y-2">
      <p className="text-sm">Upload complete.</p>
      <div className="space-x-2">
        <button
          className="rounded bg-blue-600 px-3 py-1 text-sm text-white"
          onClick={() => router.push(`/analyses/${analysisId}`)}
        >
          View analysis
        </button>
        <button
          className="rounded border px-3 py-1 text-sm"
          onClick={onReset}
        >
          Upload another
        </button>
      </div>
    </div>
  );
}
