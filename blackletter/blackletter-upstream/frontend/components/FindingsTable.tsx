'use client';

import { useState, useMemo } from 'react';
import VerdictChips from '@/components/VerdictChips';
import { Finding } from '@/lib/types';

interface FindingsTableProps {
  findings: Finding[];
  onRowClick: (finding: Finding) => void;
}

export default function FindingsTable({ findings, onRowClick }: FindingsTableProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [verdictFilter, setVerdictFilter] = useState<string>('all');

  // Filter findings based on search term and verdict filter
  const filteredFindings = useMemo(() => {
    return findings.filter(finding => {
      const matchesSearch = finding.detector.toLowerCase().includes(searchTerm.toLowerCase()) ||
                           finding.rationale.toLowerCase().includes(searchTerm.toLowerCase());
      
      const matchesVerdict = verdictFilter === 'all' || finding.verdict === verdictFilter;
      
      return matchesSearch && matchesVerdict;
    });
  }, [findings, searchTerm, verdictFilter]);

  return (
    <div>
      {/* Search and Filter Controls */}
      <div className="mb-4 flex flex-col sm:flex-row gap-4">
        <input
          type="text"
          placeholder="Search detectors or rationale..."
          className="border p-2 rounded flex-grow"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <select
          className="border p-2 rounded"
          value={verdictFilter}
          onChange={(e) => setVerdictFilter(e.target.value)}
        >
          <option value="all">All Verdicts</option>
          <option value="pass">Pass</option>
          <option value="weak">Weak</option>
          <option value="missing">Missing</option>
          <option value="needs_review">Needs Review</option>
        </select>
      </div>

      {/* Findings Table */}
      <div className="overflow-x-auto">
        {filteredFindings.length === 0 ? (
          <div className="text-center p-8 border rounded">
            <p className="text-gray-500">No findings match the current filters.</p>
          </div>
        ) : (
          <table className="min-w-full bg-white border">
            <thead>
              <tr className="bg-gray-100">
                <th className="py-2 px-4 border-b text-left">Detector</th>
                <th className="py-2 px-4 border-b text-left">Verdict</th>
                <th className="py-2 px-4 border-b text-left">Rationale</th>
              </tr>
            </thead>
            <tbody>
              {filteredFindings.map((finding) => (
                <tr 
                  key={finding.id} 
                  className="hover:bg-gray-50 cursor-pointer"
                  onClick={() => onRowClick(finding)}
                >
                  <td className="py-2 px-4 border-b">{finding.detector}</td>
                  <td className="py-2 px-4 border-b">
                    <VerdictChips verdict={finding.verdict} />
                  </td>
                  <td className="py-2 px-4 border-b">{finding.rationale}</td>
                  {/* Add more columns as needed */}
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </div>
  );
}