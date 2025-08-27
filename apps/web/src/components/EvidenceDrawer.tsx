"use client";

import type { Finding } from "@/lib/types";
import { anchorTermsFor } from "@/lib/anchors";
import { useEffect, useRef } from "react";

type Props = {
  finding: Finding | null;
  onClose: () => void;
  onMarkReviewed?: (f: Finding) => void;
};

export default function EvidenceDrawer({ finding, onClose, onMarkReviewed }: Props) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const closeRef = useRef<HTMLButtonElement | null>(null);
  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") onClose();
    }
    window.addEventListener("keydown", onKey);
    // focus close button on open for keyboard users
    closeRef.current?.focus();
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  if (!finding) return null;
  return (
    <div
      role="dialog"
      aria-modal="true"
      className="fixed inset-0 z-50 bg-black/30 flex justify-end"
      onClick={onClose}
    >
      <div
        ref={containerRef}
        className="w-full max-w-xl h-full bg-white dark:bg-zinc-900 shadow-xl p-6 overflow-y-auto focus:outline-none"
        onClick={(e) => e.stopPropagation()}
        tabIndex={-1}
      >
        <div className="flex items-start justify-between mb-4">
          <div>
            <h2 className="text-lg font-semibold">{finding.detector_id}</h2>
            <p className="text-xs text-gray-500">Rule: {finding.rule_id}</p>
          </div>
          <button
            aria-label="Close"
            className="rounded border px-2 py-1 text-sm focus:ring-2 focus:ring-offset-2 focus:ring-black"
            onClick={onClose}
            ref={closeRef}
          >
            Close
          </button>
        </div>
        <div className="space-y-3">
          <div>
            <h3 className="text-sm font-medium">Snippet</h3>
            <pre className="mt-1 whitespace-pre-wrap text-sm bg-black/5 dark:bg-white/10 p-3 rounded">
              {highlightTerms(finding.snippet, anchorTermsFor(finding.detector_id))}
            </pre>
            <p className="text-xs text-gray-500 mt-1">
              page {finding.page} • offsets {finding.start}–{finding.end}
            </p>
          </div>
          <div>
            <h3 className="text-sm font-medium">Why</h3>
            <ul className="list-disc list-inside text-sm text-gray-700 dark:text-gray-200">
              <li>{finding.rationale}</li>
            </ul>
          </div>
          <div className="flex gap-2">
            <button
              className="rounded bg-black text-white px-3 py-1 text-sm"
              onClick={() => navigator.clipboard.writeText(finding.snippet)}
            >
              Copy snippet
            </button>
            {onMarkReviewed && !finding.reviewed && (
              <button
                className="rounded border px-3 py-1 text-sm"
                onClick={() => onMarkReviewed(finding)}
              >
                Mark reviewed
              </button>
            )}
            {finding.reviewed && (
              <span className="text-xs text-emerald-700">Reviewed</span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

function highlightTerms(text: string, terms: string[]) {
  if (!terms.length) return text;
  const escaped = terms
    .filter(Boolean)
    .map((t) => t.replace(/[.*+?^${}()|[\]\\]/g, "\\$&"));
  if (!escaped.length) return text;
  const regex = new RegExp(`(${escaped.join("|")})`, "gi");
  const parts = text.split(regex);
  return parts.map((part, i) => {
    const isMatch = terms.some((t) => part.toLowerCase() === t.toLowerCase());
    return isMatch ? (
      <mark key={i} className="bg-yellow-200 text-yellow-900 rounded px-0.5">
        {part}
      </mark>
    ) : (
      <span key={i}>{part}</span>
    );
  });
}
