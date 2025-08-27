"use client";

import { useMemo, useState } from "react";
import type { Finding, Verdict } from "@/lib/types";

type Props = {
  findings: Finding[];
  onSelect: (f: Finding) => void;
};

const VERDICT_LABEL: Record<Verdict, string> = {
  pass: "Pass",
  weak: "Weak",
  missing: "Missing",
  needs_review: "Needs review",
};

export default function FindingsTable({ findings, onSelect }: Props) {
  const [query, setQuery] = useState("");
  const [verdict, setVerdict] = useState<Verdict | "all">("all");

  const filtered = useMemo(() => {
    return findings.filter((f) => {
      const matchVerdict = verdict === "all" || f.verdict === verdict;
      const q = query.trim().toLowerCase();
      const matchQuery =
        !q ||
        f.snippet.toLowerCase().includes(q) ||
        f.rationale.toLowerCase().includes(q) ||
        f.detector_id.toLowerCase().includes(q);
      return matchVerdict && matchQuery;
    });
  }, [findings, query, verdict]);

  return (
    <div className="space-y-4">
      <div className="flex gap-2 items-center">
        <input
          aria-label="Search snippets"
          placeholder="Search snippets or rationale"
          className="border rounded-md px-3 py-2 text-sm w-full"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <select
          aria-label="Filter by verdict"
          className="border rounded-md px-2 py-2 text-sm"
          value={verdict}
          onChange={(e) => setVerdict(e.target.value as any)}
        >
          <option value="all">All</option>
          <option value="pass">Pass</option>
          <option value="weak">Weak</option>
          <option value="missing">Missing</option>
          <option value="needs_review">Needs review</option>
        </select>
      </div>

      <div className="border rounded-lg overflow-hidden">
        <table className="w-full text-sm" role="table">
          <thead className="bg-black/5">
            <tr>
              <th scope="col" className="text-left p-3">Detector</th>
              <th scope="col" className="text-left p-3">Verdict</th>
              <th scope="col" className="text-left p-3">Rationale</th>
              <th className="p-3" />
            </tr>
          </thead>
          <tbody>
            {filtered.length === 0 && (
              <tr>
                <td colSpan={4} className="p-6 text-center text-gray-500">
                  No results. Try adjusting filters or search.
                </td>
              </tr>
            )}
            {filtered.map((f) => (
              <tr key={`${f.detector_id}-${f.start}-${f.end}`} className="border-t">
                <td className="p-3 font-medium">{f.detector_id}</td>
                <td className="p-3">
                  <span
                    aria-label={`Verdict: ${VERDICT_LABEL[f.verdict]}`}
                    className={badgeFor(f.verdict)}
                  >
                    {VERDICT_LABEL[f.verdict]}
                  </span>
                </td>
                <td className="p-3 text-gray-600 dark:text-gray-300">
                  {f.rationale}
                </td>
                <td className="p-3 text-right">
                  <button
                    className="text-blue-600 hover:underline"
                    onClick={() => onSelect(f)}
                  >
                    View
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function badgeFor(v: Verdict) {
  switch (v) {
    case "pass":
      return "inline-flex items-center px-2 py-1 text-xs rounded bg-emerald-200 text-emerald-800";
    case "weak":
      return "inline-flex items-center px-2 py-1 text-xs rounded bg-amber-200 text-amber-900";
    case "missing":
      return "inline-flex items-center px-2 py-1 text-xs rounded bg-red-200 text-red-900";
    case "needs_review":
      return "inline-flex items-center px-2 py-1 text-xs rounded bg-sky-200 text-sky-900";
  }
}
