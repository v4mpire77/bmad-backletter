"use client";

import { useState } from "react";
import FindingsTable from "@/components/FindingsTable";
import EvidenceDrawer from "@/components/EvidenceDrawer";
import type { Finding } from "@/lib/types";

export default function FindingsClient({ initialFindings }: { initialFindings: Finding[] }) {
  const [selected, setSelected] = useState<Finding | null>(null);
  const [findings, setFindings] = useState<Finding[]>(initialFindings);

  function markReviewed(f: Finding) {
    setFindings((prev) => prev.map((x) => (x === f ? { ...x, reviewed: true } : x)));
  }

  return (
    <>
      <FindingsTable findings={findings} onSelect={setSelected} />
      <EvidenceDrawer
        finding={selected}
        onClose={() => setSelected(null)}
        onMarkReviewed={markReviewed}
      />
    </>
  );
}

