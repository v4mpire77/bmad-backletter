'use client';
import React from 'react';
import type { PageFinding } from '@/lib/types';

type Props = {
  findings: PageFinding[];
  onRowClick?: (f: PageFinding) => void;
};

export default function FindingsTable({ findings, onRowClick }: Props) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-left">
        <thead>
          <tr>
            <th className="py-2 pr-4">Rule</th>
            <th className="py-2">Snippet</th>
          </tr>
        </thead>
        <tbody>
          {findings.map((f) => (
            <tr
              key={f.id ?? `${f.rule_id}-${f.snippet.slice(0, 16)}`}
              className="cursor-pointer hover:bg-muted/50"
              onClick={() => onRowClick?.(f)}
            >
              <td className="py-2 pr-4 whitespace-nowrap">{f.rule_id}</td>
              <td className="py-2">{f.snippet}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
