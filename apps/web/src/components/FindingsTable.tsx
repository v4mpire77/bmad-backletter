'use client';

import React, { useState } from 'react';
import VerdictBadge from './VerdictBadge';
import EvidenceDrawer from './EvidenceDrawer';
import type { Finding } from '@bmad/shared/types';

interface FindingsTableProps {
  findings: Finding[];
  onFindingClick?: (finding: Finding) => void;
}

export default function FindingsTable({ findings, onFindingClick }: FindingsTableProps) {
  const [selected, setSelected] = useState<Finding | null>(null);
  const handleClose = () => setSelected(null);

  const handleRowClick = (finding: Finding) => {
    if (onFindingClick) {
      onFindingClick(finding);
    } else {
      setSelected(finding);
    }
  };

  return (
    <div className="space-y-4">
      <table className="min-w-full text-sm">
        <thead>
          <tr className="bg-gray-50 text-left">
            <th className="p-4 font-medium">Rule</th>
            <th className="p-4 font-medium">Snippet</th>
            <th className="p-4 font-medium">Verdict</th>
          </tr>
        </thead>
        <tbody>
          {findings.map(f => (
            <tr
              key={f.id}
              onClick={() => handleRowClick(f)}
              className="cursor-pointer hover:bg-gray-50"
            >
              <td className="p-4">{f.rule_id}</td>
              <td className="p-4">{f.snippet}</td>
              <td className="p-4"><VerdictBadge verdict={f.verdict} /></td>
            </tr>
          ))}
        </tbody>
      </table>
      {!onFindingClick && (
        <EvidenceDrawer isOpen={!!selected} onClose={handleClose}>
          <p><span className="font-medium">Rule:</span> {selected?.rule_id}</p>
          <p className="mt-2 whitespace-pre-wrap">{selected?.snippet}</p>
        </EvidenceDrawer>
      )}
    </div>
  );
}
