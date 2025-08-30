"use client";

import { useMemo, useState } from "react";
import type { Finding, Verdict } from "@/lib/types";
import VerdictBadge from "@/components/VerdictBadge";

type SortField = "rule_name" | "category" | "severity";
type SortDirection = "asc" | "desc";

type Props = {
  findings: Finding[];
  onSelect: (f: Finding) => void;
};

export default function FindingsTable({ findings, onSelect }: Props) {
  const [query, setQuery] = useState("");
  const [severity, setSeverity] = useState<Verdict | "all">("all");
  const [sortField, setSortField] = useState<SortField>("rule_name");
  const [sortDirection, setSortDirection] = useState<SortDirection>("asc");

  const filtered = useMemo(() => {
    const filteredFindings = findings.filter((f) => {
      const matchSeverity = severity === "all" || f.severity === severity;
      const q = query.trim().toLowerCase();
      const matchQuery =
        !q ||
        f.evidence.toLowerCase().includes(q) ||
        f.rule_name.toLowerCase().includes(q);
      return matchSeverity && matchQuery;
    });

    // Sort the filtered findings
    return filteredFindings.sort((a, b) => {
      let aValue: any;
      let bValue: any;

      switch (sortField) {
        case "rule_name":
          aValue = a.rule_name.toLowerCase();
          bValue = b.rule_name.toLowerCase();
          break;
        case "category":
          aValue = a.category.toLowerCase();
          bValue = b.category.toLowerCase();
          break;
        case "severity":
          aValue = a.severity;
          bValue = b.severity;
          break;
        default:
          return 0;
      }

      if (aValue < bValue) return sortDirection === "asc" ? -1 : 1;
      if (aValue > bValue) return sortDirection === "asc" ? 1 : -1;
      return 0;
    });
  }, [findings, query, severity, sortField, sortDirection]);

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
          aria-label="Search evidence"
          placeholder="Search evidence or rule name"
          className="border rounded-md px-3 py-2 text-sm w-full"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <select
          aria-label="Filter by severity"
          className="border rounded-md px-2 py-2 text-sm"
          value={severity}
          onChange={(e: React.ChangeEvent<HTMLSelectElement>) =>
            setSeverity(e.target.value as Verdict | "all")
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
                  onClick={() => handleSort("rule_name")}
                  aria-label={`Sort by rule name ${sortField === "rule_name" ? (sortDirection === "asc" ? "descending" : "ascending") : "ascending"}`}
                >
                  Rule {getSortIcon("rule_name")}
                </button>
              </th>
              <th scope="col" className="text-left p-3">
                <button
                  className="flex items-center gap-1 hover:bg-black/10 px-2 py-1 rounded"
                  onClick={() => handleSort("category")}
                  aria-label={`Sort by category ${sortField === "category" ? (sortDirection === "asc" ? "descending" : "ascending") : "ascending"}`}
                >
                  Category {getSortIcon("category")}
                </button>
              </th>
              <th scope="col" className="text-left p-3">
                <button
                  className="flex items-center gap-1 hover:bg-black/10 px-2 py-1 rounded"
                  onClick={() => handleSort("severity")}
                  aria-label={`Sort by severity ${sortField === "severity" ? (sortDirection === "asc" ? "descending" : "ascending") : "ascending"}`}
                >
                  Severity {getSortIcon("severity")}
                </button>
              </th>
              <th scope="col" className="text-left p-3">
                Evidence
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
              <tr key={f.finding_id} className="border-t">
                <td className="p-3 font-medium">{f.rule_name}</td>
                <td className="p-3 text-gray-600 dark:text-gray-300">
                  {f.category}
                </td>
                <td className="p-3">
                  <VerdictBadge verdict={f.severity} size="sm" />
                </td>
                <td className="p-3 text-gray-600 dark:text-gray-300">
                  {f.evidence}
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


