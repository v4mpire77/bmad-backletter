"use client";

import { useMemo, useState } from "react";
import FindingsTable from "@/components/FindingsTable";
import EvidenceDrawer from "@/components/EvidenceDrawer";
import type { Finding, Verdict } from "@/lib/types";

export default function FindingsClient({
  initialFindings,
  selectedVerdict = "all",
  onSelectVerdict,
}: {
  initialFindings: Finding[];
  selectedVerdict?: Verdict | "all";
  onSelectVerdict?: (v: Verdict | "all") => void;
}) {
  const [selected, setSelected] = useState<Finding | null>(null);
  const [findings, setFindings] = useState<Finding[]>(initialFindings);

  const filtered = useMemo(() => {
    if (selectedVerdict === "all") return findings;
    return findings.filter((f) => f.verdict === selectedVerdict);
  }, [findings, selectedVerdict]);

  function markReviewed(f: Finding) {
    setFindings((prev) => prev.map((x) => (x === f ? { ...x, reviewed: true } : x)));
  }

  return (
    <>
      <FindingsTable findings={filtered} onSelect={setSelected} />
      <EvidenceDrawer
        finding={selected}
        onClose={() => setSelected(null)}
        onMarkReviewed={markReviewed}
      />
    </>
  );
}

