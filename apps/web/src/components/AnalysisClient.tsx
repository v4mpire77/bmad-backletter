"use client";

import { useState } from "react";
import VerdictChips from "@/components/VerdictChips";
import FindingsClient from "@/components/FindingsClient";
import ExportClient from "@/components/ExportClient";
import type { AnalysisSummary, Finding, Verdict } from "@/lib/types";

type Props = {
  summary: AnalysisSummary | null;
  findings: Finding[];
  findingsError?: boolean;
  summaryError?: boolean;
};

export default function AnalysisClient({ summary, findings, findingsError, summaryError }: Props) {
  const [selectedVerdict, setSelectedVerdict] = useState<Verdict | "all">("all");

  return (
    <div>
      <header className="mb-6">
        <div className="flex items-center justify-between gap-4">
          <h1 className="text-2xl font-semibold">Findings</h1>
          <ExportClient />
        </div>
        {summary ? (
          <div className="mt-2">
            <p className="text-sm text-gray-600 dark:text-gray-300">
              {summary.filename} • {new Date(summary.created_at).toLocaleString()}
            </p>
            <div className="mt-2">
              <VerdictChips
                counts={summary.verdicts}
                selected={selectedVerdict}
                onSelect={setSelectedVerdict}
              />
            </div>
          </div>
        ) : summaryError ? (
          <div className="mt-2 rounded border border-red-200 bg-red-50 text-red-700 p-3">
            Could not load analysis summary. Please try again.
          </div>
        ) : (
          <p className="text-sm text-gray-600 dark:text-gray-300 mt-1">Loading…</p>
        )}
      </header>

      {findingsError && (
        <div className="mb-4 rounded border border-red-200 bg-red-50 text-red-700 p-3">
          Could not load findings. Please refresh or try again later.
        </div>
      )}

      <FindingsClient
        initialFindings={findings}
        selectedVerdict={selectedVerdict}
        onSelectVerdict={setSelectedVerdict}
      />
    </div>
  );
}


