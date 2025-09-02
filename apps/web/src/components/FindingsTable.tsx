'use client';

import React, { useState } from 'react';
import FindingsDrawer from './FindingsDrawer';

interface Finding {
  id: string;
  rule: string;
  evidence: string;
  verdict: string;
}

interface FindingsTableProps {
  findings: Finding[];
}

export default function FindingsTable({ findings }: FindingsTableProps) {
  const [selected, setSelected] = useState<Finding | null>(null);
  const handleClose = () => setSelected(null);

  return (
    <div className="space-y-4">
      <table className="min-w-full text-sm">
        <thead>
          <tr className="bg-gray-50 text-left">
            <th className="p-4 font-medium">Rule</th>
            <th className="p-4 font-medium">Evidence</th>
          </tr>
        </thead>
        <tbody>
          {findings.map(f => (
            <tr
              key={f.id}
              onClick={() => setSelected(f)}
              className="cursor-pointer hover:bg-gray-50"
            >
              <td className="p-4">{f.rule}</td>
              <td className="p-4">{f.evidence}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <FindingsDrawer open={!!selected} finding={selected} onClose={handleClose} />
    </div>
  );
}

