'use client';

import React, { useMemo } from 'react';

interface VerdictBadgeProps {
  verdict: string;
  variant?: 'subtle' | 'solid';
}

export default function VerdictBadge({ verdict, variant = 'subtle' }: VerdictBadgeProps) {
  const badgeStyle = useMemo(() => {
    const styles = {
      pass: {
        subtle: 'bg-green-100 text-green-800',
        solid: 'bg-green-700 text-white',
      },
      weak: {
        subtle: 'bg-yellow-100 text-yellow-800',
        solid: 'bg-yellow-800 text-white',
      },
      missing: {
        subtle: 'bg-red-100 text-red-800',
        solid: 'bg-red-700 text-white',
      },
      needs_review: {
        subtle: 'bg-blue-100 text-blue-800',
        solid: 'bg-blue-700 text-white',
      },
      default: {
        subtle: 'bg-gray-100 text-gray-800',
        solid: 'bg-gray-700 text-white',
      },
    } as const;

    const key = verdict.toLowerCase();
    const variantKey = variant ?? 'subtle';
    return styles[key as keyof typeof styles]?.[variantKey] ?? styles.default[variantKey];
  }, [verdict, variant]);

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
    <span className={`px-2 py-1 text-xs font-semibold rounded-full ${badgeStyle}`} aria-label={ariaLabel}>
      {verdict.replace('_', ' ')}
    </span>
  );
}
