export default function VerdictChip({ verdict }: { verdict: "pass" | "weak" | "missing" | "needs_review" }) {
  const cls =
    verdict === "pass"
      ? "bg-green-100 text-green-800"
      : verdict === "weak"
      ? "bg-amber-100 text-amber-800"
      : verdict === "missing"
      ? "bg-red-100 text-red-800"
      : "bg-blue-100 text-blue-800";
  return <span className={`px-2 py-0.5 rounded text-xs font-medium ${cls}`}>{verdict.replace("_", " ")}</span>;
}

