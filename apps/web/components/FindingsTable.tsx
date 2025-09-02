import VerdictBadge from "./VerdictBadge";

type Finding = {
  rule_id: string;
  rule_name: string;
  verdict: "Pass" | "Weak" | "Missing" | "Needs Review";
  snippet: string;
  page?: number | null;
  rationale?: string | null;
};

export default function FindingsTable({ findings }: { findings: Finding[] }) {
  return (
    <div className="overflow-hidden rounded-xl border bg-white">
      <table className="w-full text-sm">
        <thead className="bg-neutral-50 text-neutral-600">
          <tr>
            <th className="text-left px-4 py-3">Obligation</th>
            <th className="text-left px-4 py-3">Verdict</th>
            <th className="text-left px-4 py-3">Evidence</th>
          </tr>
        </thead>
        <tbody>
          {findings.map((f) => (
            <tr key={f.rule_id} className="border-t align-top">
              <td className="px-4 py-3">
                <div className="font-medium">{f.rule_name}</div>
                <div className="text-xs text-neutral-500">{f.rule_id}</div>
              </td>
              <td className="px-4 py-3"><VerdictBadge verdict={f.verdict} /></td>
              <td className="px-4 py-3">
                <div className="text-neutral-700">{f.snippet}</div>
                {f.rationale && <div className="text-xs text-neutral-500 mt-1">{f.rationale}</div>}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
