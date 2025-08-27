import type { VerdictCounts } from "@/lib/types";

export default function VerdictChips({ counts }: { counts: VerdictCounts }) {
  return (
    <div className="flex flex-wrap items-center gap-2" aria-label="Verdict summary">
      <Chip label="Pass" value={counts.pass_count} className="bg-emerald-200 text-emerald-800" />
      <Chip label="Weak" value={counts.weak_count} className="bg-amber-200 text-amber-900" />
      <Chip label="Missing" value={counts.missing_count} className="bg-red-200 text-red-900" />
      <Chip label="Needs review" value={counts.needs_review_count} className="bg-sky-200 text-sky-900" />
    </div>
  );
}

function Chip({ label, value, className }: { label: string; value: number; className: string }) {
  return (
    <span aria-label={`${label}: ${value}`} className={`inline-flex items-center px-2 py-1 text-xs rounded ${className}`}>
      {label[0]} {value}
    </span>
  );
}

