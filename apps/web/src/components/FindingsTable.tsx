"use client";

import { useMemo, useState } from "react";
import type { Finding, Verdict } from "@/lib/types";
import VerdictBadge from "@/components/VerdictBadge";

type SortField = "detector_id" | "verdict" | "page" | "rationale";
type SortDirection = "asc" | "desc";

type Props = {
  findings: Finding[];
  onSelect: (f: Finding) => void;
};



export default function FindingsTable({ findings, onSelect }: Props) {
  const [query, setQuery] = useState("");
  const [verdict, setVerdict] = useState<Verdict | "all">("all");
  const [sortField, setSortField] = useState<SortField>("detector_id");
  const [sortDirection, setSortDirection] = useState<SortDirection>("asc");

  const filtered = useMemo(() => {
    const filteredFindings = findings.filter((f) => {
      const matchVerdict = verdict === "all" || f.verdict === verdict;
      const q = query.trim().toLowerCase();
      const matchQuery =
        !q ||
        f.snippet.toLowerCase().includes(q) ||
        f.rationale.toLowerCase().includes(q) ||
        f.detector_id.toLowerCase().includes(q);
      return matchVerdict && matchQuery;
    });

    // Sort the filtered findings
    return filteredFindings.sort((a, b) => {
      let aValue: any;
      let bValue: any;

      switch (sortField) {
        case "detector_id":
          aValue = a.detector_id.toLowerCase();
          bValue = b.detector_id.toLowerCase();
          break;
        case "verdict":
          aValue = a.verdict;
          bValue = b.verdict;
          break;
        case "page":
          aValue = a.page;
          bValue = b.page;
          break;
        case "rationale":
          aValue = a.rationale.toLowerCase();
          bValue = b.rationale.toLowerCase();
          break;
        default:
          return 0;
      }

      if (aValue < bValue) return sortDirection === "asc" ? -1 : 1;
      if (aValue > bValue) return sortDirection === "asc" ? 1 : -1;
      return 0;
    });
  }, [findings, query, verdict, sortField, sortDirection]);

  const handleSort = (field: SortField) => {
    if (sortField === field) {
      setSortDirection(sortDirection === "asc" ? "desc" : "asc");
    } else {
      setSortField(field);
      setSortDirection("asc");
    }
  };

  const getSortIcon = (field: SortField) => {
    if (sortField !== field) return "↕️";
    return sortDirection === "asc" ? "↑" : "↓";
  };

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
          onChange={(e: React.ChangeEvent<HTMLSelectElement>) =>
            setVerdict(e.target.value as Verdict | "all")
          }
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
              <th scope="col" className="text-left p-3">
                <button
                  className="flex items-center gap-1 hover:bg-black/10 px-2 py-1 rounded"
                  onClick={() => handleSort("detector_id")}
                  aria-label={`Sort by detector ${sortField === "detector_id" ? (sortDirection === "asc" ? "descending" : "ascending") : "ascending"}`}
                >
                  Detector {getSortIcon("detector_id")}
                </button>
              </th>
              <th scope="col" className="text-left p-3">
                <button
                  className="flex items-center gap-1 hover:bg-black/10 px-2 py-1 rounded"
                  onClick={() => handleSort("verdict")}
                  aria-label={`Sort by verdict ${sortField === "verdict" ? (sortDirection === "asc" ? "descending" : "ascending") : "ascending"}`}
                >
                  Verdict {getSortIcon("verdict")}
                </button>
              </th>
              <th scope="col" className="text-left p-3">
                <button
                  className="flex items-center gap-1 hover:bg-black/10 px-2 py-1 rounded"
                  onClick={() => handleSort("rationale")}
                  aria-label={`Sort by rationale ${sortField === "rationale" ? (sortDirection === "asc" ? "descending" : "ascending") : "ascending"}`}
                >
                  Rationale {getSortIcon("rationale")}
                </button>
              </th>
              <th scope="col" className="text-left p-3">
                <button
                  className="flex items-center gap-1 hover:bg-black/10 px-2 py-1 rounded"
                  onClick={() => handleSort("page")}
                  aria-label={`Sort by page ${sortField === "page" ? (sortDirection === "asc" ? "descending" : "ascending") : "ascending"}`}
                >
                  Page {getSortIcon("page")}
                </button>
              </th>
              <th className="p-3" />
            </tr>
          </thead>
          <tbody>
            {filtered.length === 0 && (
              <tr>
                <td colSpan={5} className="p-6 text-center text-gray-500">
                  No results. Try adjusting filters or search.
                </td>
              </tr>
            )}
            {filtered.map((f) => (
              <tr key={`${f.detector_id}-${f.start}-${f.end}`} className="border-t">
                <td className="p-3 font-medium">{f.detector_id}</td>
                <td className="p-3">
                  <VerdictBadge verdict={f.verdict} size="sm" />
                </td>
                <td className="p-3 text-gray-600 dark:text-gray-300">
                  {f.rationale}
                </td>
                <td className="p-3 text-gray-600 dark:text-gray-300">
                  {f.page}
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


