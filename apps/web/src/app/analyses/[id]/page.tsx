"use client";

import React, { useState } from "react";
import useJobStatus from "@/lib/useJobStatus";
import FindingsTable from "@/components/FindingsTable";
import FindingsDrawer from "@/components/FindingsDrawer";
import type { Finding } from "@/types";

interface PageProps {
  params: { id: string };
}

export default function AnalysisDetailPage({ params }: PageProps) {
  const { status, findings, error } = useJobStatus(params.id);
  const [selected, setSelected] = useState<Finding | null>(null);

  const handleSelect = (f: Finding) => setSelected(f);
  const handleClose = () => setSelected(null);

  if (error) {
    return <p className="text-sm text-red-500">{error}</p>;
  }

  return (
    <div className="space-y-3">
      <h1 className="text-2xl font-semibold">Analysis {params.id}</h1>
      {status !== "done" ? (
        <p className="text-sm text-muted-foreground">
          Status: {status.charAt(0).toUpperCase() + status.slice(1)}
        </p>
      ) : findings && findings.length > 0 ? (
        <>
          <FindingsTable findings={findings} onSelect={handleSelect} />
          <FindingsDrawer
            open={!!selected}
            onClose={handleClose}
            finding={
              selected && {
                rule: selected.rule_id,
                evidence: selected.snippet,
                verdict: selected.verdict,
              }
            }
          />
        </>
      ) : (
        <p className="text-sm text-muted-foreground">No findings.</p>
      )}
    </div>
  );
}
