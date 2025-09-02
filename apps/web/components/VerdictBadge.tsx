type Verdict = "Pass" | "Weak" | "Missing" | "Needs Review";
export default function VerdictBadge({ verdict }: { verdict: Verdict }) {
  const color =
    verdict === "Pass" ? "bg-green-600" :
    verdict === "Weak" ? "bg-amber-500" :
    verdict === "Needs Review" ? "bg-rose-600" : "bg-neutral-500";
  return <span className={`text-white text-xs px-2 py-1 rounded ${color}`}>{verdict}</span>;
}
