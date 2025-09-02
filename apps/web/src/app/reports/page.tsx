'use client';

import React from 'react';
import { useExportStore } from '../../lib/exportStore';

export default function ReportsPage() {
  const reports = useExportStore();

  return (
    <main className="p-4">
      <h1 className="text-xl font-bold">Reports</h1>
      {reports.length === 0 ? (
        <p>No reports exported yet.</p>
      ) : (
        <ul className="mt-4 space-y-2">
          {reports.map((r) => (
            <li key={r.id} className="rounded border p-2">
              <span className="font-medium">{r.name}</span>
              <span className="ml-2 text-sm text-gray-500">
                {new Date(r.createdAt).toLocaleString()}
              </span>
            </li>
          ))}
        </ul>
      )}
    </main>
  );
}
