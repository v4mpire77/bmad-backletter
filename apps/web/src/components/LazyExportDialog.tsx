'use client';

import React, { Suspense, lazy } from 'react';

// Lazy load the ExportDialog component
const ExportDialog = lazy(() => import('./ExportDialog'));

interface LazyExportDialogProps {
  isOpen: boolean;
  onClose: () => void;
}

// Loading fallback component
const DialogSkeleton = () => (
  <div className="fixed inset-0 z-50 flex items-center justify-center">
    <div className="fixed inset-0 bg-black/50" />
    <div className="relative z-10 rounded bg-white p-4 shadow-md">
      <div className="animate-pulse">
        <div className="h-4 bg-gray-200 rounded mb-4"></div>
        <div className="flex justify-end gap-2">
          <div className="h-8 w-16 bg-gray-200 rounded"></div>
          <div className="h-8 w-16 bg-gray-200 rounded"></div>
        </div>
      </div>
    </div>
  </div>
);

export default function LazyExportDialog(props: LazyExportDialogProps) {
  if (!props.isOpen) return null;

  return (
    <Suspense fallback={<DialogSkeleton />}>
      <ExportDialog {...props} />
    </Suspense>
  );
}