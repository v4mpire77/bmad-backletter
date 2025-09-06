'use client';

import React, { Suspense, lazy } from 'react';

// Lazy load the FindingsDrawer component
const FindingsDrawer = lazy(() => import('./FindingsDrawer'));

interface LazyFindingsDrawerProps {
  open: boolean;
  onClose: () => void;
  finding?: {
    rule: string;
    evidence: string;
    verdict?: string;
  } | null;
}

// Loading fallback component
const DrawerSkeleton = () => (
  <div className="fixed inset-0 z-50">
    <div className="fixed inset-0 bg-black/50" />
    <div className="absolute right-0 top-0 h-full w-80 bg-white p-6 shadow-lg space-y-4">
      <div className="animate-pulse">
        <div className="h-6 bg-gray-200 rounded mb-2"></div>
        <div className="h-4 bg-gray-200 rounded mb-1"></div>
        <div className="h-4 bg-gray-200 rounded mb-1"></div>
        <div className="h-4 bg-gray-200 rounded"></div>
      </div>
    </div>
  </div>
);

export default function LazyFindingsDrawer(props: LazyFindingsDrawerProps) {
  if (!props.open) return null;

  return (
    <Suspense fallback={<DrawerSkeleton />}>
      <FindingsDrawer {...props} />
    </Suspense>
  );
}