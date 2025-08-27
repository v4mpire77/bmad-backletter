import { getMockAnalyses } from "@/lib/mocks";
import DemoBanner from "@/components/DemoBanner";
import type { AnalysisSummary } from "@/lib/types";

async function fetchAnalyses(): Promise<AnalysisSummary[]> {
  if (process.env.NEXT_PUBLIC_USE_MOCKS === "1") {
    const items = getMockAnalyses(10);
    // Ensure the first item is ACME_DPA_MOCK.pdf with id mock-1
    if (items.length) {
      items[0] = {
        ...items[0],
        id: "mock-1",
        filename: "ACME_DPA_MOCK.pdf",
      };
    }
    return items;
  }
  const base =
    process.env.NEXT_PUBLIC_API_BASE ||
    process.env.NEXT_PUBLIC_API_URL ||
    "http://localhost:8000";
  try {
    const res = await fetch(`${base}/api/analyses?limit=50`, { cache: "no-store" });
    if (!res.ok) return [];
    return (await res.json()) as AnalysisSummary[];
  } catch {
    return [];
  }
}

export default async function DashboardPage() {
  const analyses = await fetchAnalyses();

  if (!analyses.length) {
    return (
      <div className="mx-auto max-w-3xl p-8 text-center">
        <h1 className="text-2xl font-semibold mb-4">Dashboard</h1>
        <p className="text-sm text-gray-500 mb-6">
          No analyses yet. Drag a contract to start.
        </p>
        <a
          href="/new"
          className="inline-block rounded-md bg-black text-white px-4 py-2 text-sm hover:opacity-90"
        >
          New Analysis
        </a>
      </div>
    );
  }

  return (
    <div className="mx-auto max-w-5xl p-8">
      <DemoBanner />
      <h1 className="text-2xl font-semibold mb-6">Recent Analyses</h1>
      <div className="border rounded-lg overflow-hidden">
        <table className="w-full text-sm">
          <thead className="bg-black/5">
            <tr>
              <th className="text-left p-3">Filename</th>
              <th className="text-left p-3">Created</th>
              <th className="text-left p-3">Size</th>
              <th className="text-left p-3">Verdicts</th>
              <th className="p-3" />
            </tr>
          </thead>
          <tbody>
            {analyses.map((a) => (
              <tr key={a.id} className="border-t">
                <td className="p-3">{a.filename}</td>
                <td className="p-3">{new Date(a.created_at).toLocaleString()}</td>
                <td className="p-3">{Math.round(a.size / 1024)} KB</td>
                <td className="p-3">
                  <span aria-label="Pass" className="mr-2">P {a.verdicts.pass_count}</span>
                  <span aria-label="Weak" className="mr-2">W {a.verdicts.weak_count}</span>
                  <span aria-label="Missing" className="mr-2">M {a.verdicts.missing_count}</span>
                  <span aria-label="Needs review">R {a.verdicts.needs_review_count}</span>
                </td>
                <td className="p-3 text-right">
                  <a
                    href={`/analyses/${a.id}`}
                    className="text-blue-600 hover:underline"
                  >
                    Open
                  </a>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
