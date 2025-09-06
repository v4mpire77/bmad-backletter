'use client';

import React, { useState, useEffect } from 'react';

export default function AnalysesPage() {
  const [items, setItems] = useState<{ id: string; name: string; status: 'pending' | 'complete' }[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const fetchAnalyses = async () => {
      try {
        const response = await fetch('/api/analyses');
        if (!response.ok) {
          throw new Error('Failed to fetch analyses');
        }
        const data = await response.json();
        setItems(data.map((a: any) => ({
          id: a.id,
          name: a.name,
          status: a.status,
        })));
      } catch (err) {
        setError('Failed to load analyses. Please try again later.');
        console.error('Error loading analyses:', err);
      } finally {
        setLoading(false);
      }
    };

    fetchAnalyses();
  }, []);

  if (loading) {
    return (
      <div className="space-y-3">
        <h1 className="text-2xl font-semibold">Analyses</h1>
        <p className="text-sm text-muted-foreground">Loading...</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <h1 className="text-2xl font-semibold">Analyses</h1>
      {error ? (
        <p className="text-sm text-red-500">{error}</p>
      ) : items.length === 0 ? (
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

