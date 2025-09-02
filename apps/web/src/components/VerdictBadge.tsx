'use client';

import React, { useMemo } from 'react';
import type { Finding } from '../types';

interface VerdictBadgeProps {
  verdict: Finding['verdict'] | string;
}

export default function VerdictBadge({ verdict }: VerdictBadgeProps) {
  const normalized = verdict.toLowerCase() as Finding['verdict'];

  const style = useMemo(() => {
    switch (normalized) {
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
  }, [normalized]);

  const label = useMemo(() => {
    switch (normalized) {
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
  }, [normalized]);

  return (
    <span
      className={`inline-block rounded px-2 py-1 text-xs font-semibold ${style}`}
      aria-label={label}
    >
      {verdict.replace('_', ' ')}
    </span>
  );
}
