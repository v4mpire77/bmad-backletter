"use client";

import type { Finding } from "@/lib/types";
import { anchorTermsFor } from "@/lib/anchors";
import { useEffect, useRef } from "react";
import { useFocusTrap } from "@/lib/useFocusTrap";

type Props = {
  finding: Finding | null;
  onClose: () => void;
  onMarkReviewed?: (f: Finding) => void;
};

export default function EvidenceDrawer({ finding, onClose, onMarkReviewed }: Props) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const closeRef = useRef<HTMLButtonElement | null>(null);

  const isOpen = finding !== null;
  useFocusTrap(containerRef, isOpen);

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") onClose();
    }
    if (isOpen) {
      window.addEventListener("keydown", onKey);
      // focus close button on open for keyboard users
      closeRef.current?.focus();
    }
    return () => window.removeEventListener("keydown", onKey);
  }, [isOpen, onClose]);

  if (!finding) return null;
  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="evidence-title"
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
            <h2 id="evidence-title" className="text-lg font-semibold">{finding.rule_name}</h2>
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
            <div className="flex items-center justify-between mb-2">
              <h3 className="text-sm font-medium">Evidence</h3>
              <div className="flex gap-2">
                <button
                  className="text-xs px-2 py-1 bg-gray-100 hover:bg-gray-200 dark:bg-gray-800 dark:hover:bg-gray-700 rounded transition-colors"
                  onClick={() => navigator.clipboard.writeText(finding.evidence)}
                  aria-label="Copy exact evidence"
                  title="Copy exact evidence text"
                >
                  Copy
                </button>
              </div>
            </div>
            <div className="relative">
              <pre className="whitespace-pre-wrap text-sm bg-black/5 dark:bg-white/10 p-3 rounded border">
                {highlightTerms(finding.evidence, anchorTermsFor(finding.rule_id))}
              </pre>
              <button
                className="absolute top-2 right-2 text-gray-400 hover:text-gray-600 dark:hover:text-gray-300 transition-colors"
                onClick={() => navigator.clipboard.writeText(finding.evidence)}
                aria-label="Copy evidence to clipboard"
                title="Copy to clipboard"
              >
                📋
              </button>
            </div>
            <div className="text-xs text-gray-500 mt-1 flex items-center justify-between">
              <span>offsets {finding.start}–{finding.end}</span>
              <span className="text-gray-400">
                {finding.evidence.length} characters
              </span>
            </div>
          </div>
          <div>
            <h3 className="text-sm font-medium">Text</h3>
            <ul className="list-disc list-inside text-sm text-gray-700 dark:text-gray-200">
              <li>{finding.text}</li>
            </ul>
          </div>
          <div className="flex gap-2 items-center">
            {onMarkReviewed && !finding.reviewed && (
              <button
                className="rounded bg-blue-600 hover:bg-blue-700 text-white px-3 py-1 text-sm transition-colors"
                onClick={() => onMarkReviewed(finding)}
                aria-label="Mark this finding as reviewed"
              >
                Mark as Reviewed
              </button>
            )}
            {finding.reviewed && (
              <span
                className="text-xs text-emerald-700 bg-emerald-50 px-2 py-1 rounded"
                aria-label="This finding has been reviewed"
              >
                ✓ Reviewed
              </span>
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
      <mark
        key={i}
        className="bg-yellow-200 text-yellow-900 rounded px-0.5 font-medium"
        title={`Matched term: ${part}`}
      >
        {part}
      </mark>
    ) : (
      <span key={i}>{part}</span>
    );
  });
}
