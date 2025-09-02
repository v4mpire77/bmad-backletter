'use client';

import React, { useEffect, useState } from 'react';
import Link from 'next/link';

interface Analysis {
  id: string;
  name: string;
  status: 'pending' | 'complete';
}

function statusStyle(status: Analysis['status']) {
  switch (status) {
    case 'complete':
      return 'bg-green-100 text-green-800';
    case 'pending':
      return 'bg-yellow-100 text-yellow-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
}

export default function AnalysesPage() {
  const [items, setItems] = useState<Analysis[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const load = async () => {
      try {
        const res = await fetch('/api/analyses');
        if (!res.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await res.json();
        setItems(data);
      } catch {
        setError('Failed to load analyses.');
      } finally {
        setLoading(false);
      }
    };

    load();
  }, []);

  return (
    <div className="space-y-3">
      <h1 className="text-2xl font-semibold">Analyses</h1>
      {loading ? (
        <p className="text-sm text-muted-foreground">Loading...</p>
      ) : error ? (
        <p className="text-sm text-red-500">{error}</p>
      ) : items.length === 0 ? (
        <p className="text-sm text-muted-foreground">No analyses yet.</p>
      ) : (
        <ul className="divide-y rounded-2xl border">
          {items.map(a => (
            <li key={a.id}>
              <Link
                href={`/analyses/${a.id}`}
                className="flex items-center justify-between p-4 block"
              >
                <span>{a.name}</span>
                <span
                  className={`px-2 py-1 text-xs font-semibold rounded-full ${statusStyle(
                    a.status,
                  )}`}
                >
                  {a.status.charAt(0).toUpperCase() + a.status.slice(1)}
                </span>
              </Link>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

