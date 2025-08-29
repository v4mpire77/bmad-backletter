import type { Verdict, VerdictCounts } from "@/lib/types";

type ChipVerdict = Verdict | "all";

export default function VerdictChips({
  counts,
  selected = "all",
  onSelect,
}: {
  counts: VerdictCounts;
  selected?: ChipVerdict;
  onSelect?: (v: ChipVerdict) => void;
}) {
  const total =
    counts.pass_count + counts.weak_count + counts.missing_count + counts.needs_review_count;

  return (
    <div className="flex flex-wrap items-center gap-2" aria-label="Verdict summary">
      <Chip
        label="All"
        value={total}
        active={selected === "all"}
        className="bg-gray-200 text-gray-900"
        onClick={() => onSelect?.("all")}
      />
      <Chip
        label="Pass"
        value={counts.pass_count}
        active={selected === "pass"}
        className="bg-emerald-200 text-emerald-800"
        onClick={() => onSelect?.("pass")}
      />
      <Chip
        label="Weak"
        value={counts.weak_count}
        active={selected === "weak"}
        className="bg-amber-200 text-amber-900"
        onClick={() => onSelect?.("weak")}
      />
      <Chip
        label="Missing"
        value={counts.missing_count}
        active={selected === "missing"}
        className="bg-red-200 text-red-900"
        onClick={() => onSelect?.("missing")}
      />
      <Chip
        label="Needs review"
        value={counts.needs_review_count}
        active={selected === "needs_review"}
        className="bg-sky-200 text-sky-900"
        onClick={() => onSelect?.("needs_review")}
      />
    </div>
  );
}

function Chip({
  label,
  value,
  className,
  active,
  onClick,
}: {
  label: string;
  value: number;
  className: string;
  active?: boolean;
  onClick?: () => void;
}) {
  const base = `inline-flex items-center px-2 py-1 text-xs rounded focus:outline-none focus:ring-2 focus:ring-offset-2 ${className}`;
  const style = active ? `${base} ring-2 ring-offset-2 ring-black` : base;
  return (
    <button
      type="button"
      aria-label={`${label}: ${value}`}
      className={style}
      onClick={onClick}
      data-testid={`chip-${label.toLowerCase().replace(/\s+/g, "-")}`}
    >
      {label[0]} {value}
    </button>
  );
}

