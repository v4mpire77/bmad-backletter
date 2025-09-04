import React from 'react';

export const dynamic = 'force-dynamic';

export default async function AnalysesPage() {
  const response = await fetch('/api/analyses').then(r => r.json());
  const items: { id: string; name: string; status: 'pending' | 'complete' }[] =
    response.map((a: any) => ({
      id: a.id,
      name: a.name,
      status: a.status,
    }));

  return (
    <div className="space-y-3">
      <h1 className="text-2xl font-semibold">Analyses</h1>
      {items.length === 0 ? (
        <p className="text-sm text-muted-foreground">No analyses yet.</p>
      ) : (
        <ul className="divide-y rounded-2xl border">
          {items.map(a => (
            <li key={a.id} className="flex items-center justify-between p-4">
              <span>{a.name}</span>
              <span
                className={`px-2 py-1 text-xs font-semibold rounded-full ${
                  a.status === 'complete'
                    ? 'bg-green-100 text-green-800'
                    : 'bg-yellow-100 text-yellow-800'
                }`}
              >
                {a.status.charAt(0).toUpperCase() + a.status.slice(1)}
              </span>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

