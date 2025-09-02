'use client';

import { useEffect, useState } from 'react';

type Finding = {
  rule_id: string;
  verdict: string;
  snippet: string;
};

export default function AnalysisFindingsPage({ params }: { params: { jobId: string } }) {
  const [findings, setFindings] = useState<Finding[]>([]);

  useEffect(() => {
    fetch(`/api/findings?job_id=${params.jobId}`)
      .then((res) => res.json())
      .then((data) => setFindings(data))
      .catch(() => setFindings([]));
  }, [params.jobId]);

  return (
    <div className="p-4">
      <h1 className="text-2xl font-bold mb-4">Findings</h1>
      <table className="min-w-full text-left border">
        <thead>
          <tr>
            <th className="border px-2 py-1">Rule</th>
            <th className="border px-2 py-1">Verdict</th>
            <th className="border px-2 py-1">Snippet</th>
          </tr>
        </thead>
        <tbody>
          {findings.map((f, idx) => (
            <tr key={idx}>
              <td className="border px-2 py-1">{f.rule_id}</td>
              <td className="border px-2 py-1">{f.verdict}</td>
              <td className="border px-2 py-1">{f.snippet}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
