import { getAnalyses } from "@/lib/api";
import DemoBanner from "@/components/DemoBanner";

export default async function DashboardPage() {
  const analyses = await getAnalyses(10);

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
                  <div className="flex flex-wrap gap-1">
                    {a.verdicts.pass_count > 0 && (
                      <span className="text-xs bg-emerald-100 text-emerald-800 px-2 py-1 rounded">
                        Pass: {a.verdicts.pass_count}
                      </span>
                    )}
                    {a.verdicts.weak_count > 0 && (
                      <span className="text-xs bg-amber-100 text-amber-800 px-2 py-1 rounded">
                        Weak: {a.verdicts.weak_count}
                      </span>
                    )}
                    {a.verdicts.missing_count > 0 && (
                      <span className="text-xs bg-red-100 text-red-800 px-2 py-1 rounded">
                        Missing: {a.verdicts.missing_count}
                      </span>
                    )}
                    {a.verdicts.needs_review_count > 0 && (
                      <span className="text-xs bg-sky-100 text-sky-800 px-2 py-1 rounded">
                        Review: {a.verdicts.needs_review_count}
                      </span>
                    )}
                  </div>
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
