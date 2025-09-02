import { getFindings } from "@/lib/api";
import FindingsTable from "@/components/FindingsTable";

export default async function AnalysisPage({ params }: { params: { jobId: string } }) {
  const data = await getFindings(params.jobId); // throws 409 until complete; caller route is only navigated post-completion
  return (
    <section className="space-y-6">
      <header>
        <h1 className="text-2xl font-semibold">Findings</h1>
        <p className="text-sm text-neutral-600">Job ID: {params.jobId} • Rulepack {data.rulepack_version ?? "—"}</p>
      </header>
      <FindingsTable findings={data.findings} />
    </section>
  );
}
