import { useMemo, useState } from "react";
import type { Finding } from "@/hooks/useFindings";
import VerdictChip from "./VerdictChip";
import EvidenceDrawer from "./EvidenceDrawer";

export default function FindingsTable({ findings }: { findings: Finding[] }) {
  const [selected, setSelected] = useState<Finding | null>(null);
  const [filter, setFilter] = useState<"all" | Finding["verdict"]>("all");

  const rows = useMemo(
    () => (filter === "all" ? findings : findings.filter((f) => f.verdict === filter)),
    [findings, filter],
  );

  return (
    <div className="space-y-4">
      <div className="flex items-center gap-2">
        <label className="text-sm">Filter:</label>
        <select
          className="border rounded px-2 py-1 text-sm"
          value={filter}
          onChange={(e) => setFilter(e.target.value as any)}
          aria-label="Filter by verdict"
        >
          <option value="all">all</option>
          <option value="pass">pass</option>
          <option value="weak">weak</option>
          <option value="missing">missing</option>
          <option value="needs_review">needs review</option>
        </select>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-gray-600">
              <th className="py-2 pr-3">Obligation</th>
              <th className="py-2 pr-3">Verdict</th>
              <th className="py-2">Snippet</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((f, i) => (
              // eslint-disable-next-line react/no-array-index-key
              <tr
                key={`${f.rule_id}-${i}`}
                className="border-t hover:bg-gray-50 cursor-pointer"
                onClick={() => setSelected(f)}
              >
                <td className="py-2 pr-3 whitespace-nowrap">{f.rule_id}</td>
                <td className="py-2 pr-3"><VerdictChip verdict={f.verdict} /></td>
                <td className="py-2 text-gray-700 truncate">{f.snippet}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <EvidenceDrawer finding={selected} onClose={() => setSelected(null)} />
    </div>
  );
}

