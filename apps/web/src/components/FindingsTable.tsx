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
  sortState?: {
    column: 'rule' | 'verdict';
    direction: 'asc' | 'desc';
  };
  filterText?: string;
}

export default function FindingsTable({ findings, sortState = { column: 'rule', direction: 'asc' }, filterText = '' }: FindingsTableProps) {
  const [selected, setSelected] = useState<Finding | null>(null);
  const [sort, setSort] = useState(sortState);
  const [filter, setFilter] = useState(filterText);

  const handleClose = () => setSelected(null);

  const toggleSort = (column: 'rule' | 'verdict') => {
    setSort(prev => ({
      column,
      direction: prev.column === column && prev.direction === 'asc' ? 'desc' : 'asc',
    }));
  };

  const filteredFindings = findings.filter(f => {
    const term = filter.toLowerCase();
    return (
      f.rule.toLowerCase().includes(term) ||
      f.verdict.toLowerCase().includes(term)
    );
  });

  const sortedFindings = [...filteredFindings].sort((a, b) => {
    const aVal = a[sort.column].toLowerCase();
    const bVal = b[sort.column].toLowerCase();
    if (aVal < bVal) return sort.direction === 'asc' ? -1 : 1;
    if (aVal > bVal) return sort.direction === 'asc' ? 1 : -1;
    return 0;
  });

  return (
    <div className="space-y-4">
      <input
        type="text"
        placeholder="Filter by rule or verdict"
        className="border p-2 rounded w-full"
        value={filter}
        onChange={e => setFilter(e.target.value)}
      />
      <table className="min-w-full text-sm">
        <thead>
          <tr className="bg-gray-50 text-left">
            <th className="p-4 font-medium">
              <button onClick={() => toggleSort('rule')}>
                Rule {sort.column === 'rule' ? (sort.direction === 'asc' ? '▲' : '▼') : ''}
              </button>
            </th>
            <th className="p-4 font-medium">
              <button onClick={() => toggleSort('verdict')}>
                Verdict {sort.column === 'verdict' ? (sort.direction === 'asc' ? '▲' : '▼') : ''}
              </button>
            </th>
            <th className="p-4 font-medium">Evidence</th>
          </tr>
        </thead>
        <tbody>
          {sortedFindings.map(f => (
            <tr
              key={f.id}
              onClick={() => setSelected(f)}
              className="cursor-pointer hover:bg-gray-50"
            >
              <td className="p-4">{f.rule}</td>
              <td className="p-4">{f.verdict}</td>
              <td className="p-4">{f.evidence}</td>
            </tr>
          ))}
        </tbody>
      </table>
      <FindingsDrawer open={!!selected} finding={selected} onClose={handleClose} />
    </div>
  );
}

