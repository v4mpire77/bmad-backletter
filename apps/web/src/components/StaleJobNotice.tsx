'use client';
import React from 'react';

type Props = {
  jobId: string;
  onRetry: () => void;
  onCancel: () => void;
};

export const StaleJobNotice: React.FC<Props> = ({ jobId, onRetry, onCancel }) => {
  return (
    <div role="alert" className="p-4 bg-yellow-50 border border-yellow-200 rounded">
      <p className="mb-2 text-sm">
        Job {jobId} is taking longer than expected.
      </p>
      <div className="space-x-2">
        <button onClick={onRetry} className="px-2 py-1 text-xs bg-blue-600 text-white rounded">
          Retry
        </button>
        <button onClick={onCancel} className="px-2 py-1 text-xs bg-gray-200 rounded">
          Cancel
        </button>
      </div>
    </div>
  );
};
