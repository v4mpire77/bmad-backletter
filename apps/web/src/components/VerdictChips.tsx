'use client';

import React, { useMemo } from 'react';

interface VerdictChipsProps {
  verdict: string;
}

export default function VerdictChips({ verdict }: VerdictChipsProps) {
  const chipStyle = useMemo(() => {
    switch (verdict.toLowerCase()) {
      case 'pass':
        return 'bg-green-100 text-green-800';
      case 'weak':
        return 'bg-yellow-100 text-yellow-800';
      case 'missing':
        return 'bg-red-100 text-red-800';
      case 'needs_review':
        return 'bg-blue-100 text-blue-800';
      default:
        return 'bg-gray-100 text-gray-800';
    }
  }, [verdict]);

  const ariaLabel = useMemo(() => {
    switch (verdict.toLowerCase()) {
      case 'pass':
        return 'Pass';
      case 'weak':
        return 'Weak';
      case 'missing':
        return 'Missing';
      case 'needs_review':
        return 'Needs Review';
      default:
        return 'Unknown';
    }
  }, [verdict]);

  return (
    <span className={`px-2 py-1 text-xs font-semibold rounded-full ${chipStyle}`} aria-label={ariaLabel}>
      {verdict.replace('_', ' ')}
    </span>
  );
}
