"use client";

import type { Verdict } from "@/lib/types";

type Props = {
  verdict: Verdict;
  size?: "sm" | "md" | "lg";
  showLabel?: boolean;
  className?: string;
};

const VERDICT_LABELS: Record<Verdict, string> = {
  pass: "Pass",
  weak: "Weak",
  missing: "Missing",
  needs_review: "Needs review",
};

const VERDICT_DESCRIPTIONS: Record<Verdict, string> = {
  pass: "This requirement has been satisfied with strong language",
  weak: "This requirement contains weak or conditional language",
  missing: "This requirement is not present in the document",
  needs_review: "This finding requires manual review",
};

const VERDICT_COLORS: Record<Verdict, string> = {
  pass: "bg-emerald-100 text-emerald-800 border-emerald-200",
  weak: "bg-amber-100 text-amber-800 border-amber-200",
  missing: "bg-red-100 text-red-800 border-red-200",
  needs_review: "bg-sky-100 text-sky-800 border-sky-200",
};

const VERDICT_SIZE_CLASSES = {
  sm: "px-2 py-1 text-xs",
  md: "px-2.5 py-1.5 text-sm",
  lg: "px-3 py-2 text-base",
};

export default function VerdictBadge({
  verdict,
  size = "sm",
  showLabel = true,
  className = ""
}: Props) {
  const label = VERDICT_LABELS[verdict];
  const description = VERDICT_DESCRIPTIONS[verdict];
  const colors = VERDICT_COLORS[verdict];
  const sizeClasses = VERDICT_SIZE_CLASSES[size];

  return (
    <span
      role="status"
      aria-label={`${label}: ${description}`}
      aria-live="polite"
      className={`
        inline-flex items-center gap-1.5 rounded-md border font-medium
        transition-colors duration-200
        ${colors}
        ${sizeClasses}
        ${className}
      `}
      title={description}
    >
      <span
        aria-hidden="true"
        className="w-2 h-2 rounded-full bg-current opacity-60"
      />
      {showLabel && (
        <span className="leading-none">
          {label}
        </span>
      )}
    </span>
  );
}

// Convenience component for displaying verdict counts
export function VerdictBadgeGroup({
  counts,
  size = "sm",
  showLabels = true
}: {
  counts: Record<Verdict, number>;
  size?: "sm" | "md" | "lg";
  showLabels?: boolean;
}) {
  const verdicts: Verdict[] = ["pass", "weak", "missing", "needs_review"];

  return (
    <div
      role="group"
      aria-label="Verdict summary"
      className="flex flex-wrap items-center gap-2"
    >
      {verdicts.map((verdict) => {
        const count = counts[verdict];
        if (count === 0) return null;

        return (
          <div key={verdict} className="flex items-center gap-1">
            <VerdictBadge
              verdict={verdict}
              size={size}
              showLabel={showLabels}
            />
            <span
              aria-label={`${VERDICT_LABELS[verdict]} count: ${count}`}
              className="text-sm font-medium text-gray-600"
            >
              {count}
            </span>
          </div>
        );
      })}
    </div>
  );
}