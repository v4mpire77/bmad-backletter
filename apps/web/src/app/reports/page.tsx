import React from 'react';
import { getReports } from '../../lib/mockReports';

export default function ReportsPage() {
  const reports = getReports();
  return (
    <main className="p-4">
      <h1 className="text-xl font-bold">Reports</h1>
      {reports.length === 0 ? (
        <p>Report history will appear here.</p>
      ) : (
        <ul>
          {reports.map((r) => (
            <li key={r.id}>Report {r.id}</li>
          ))}
        </ul>
      )}
    </main>
  );
}
