'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { getMockExports } from '@/lib/mockStore';

export default function ReportsPage() {
  const router = useRouter();
  const [exports, setExports] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check if mocks are enabled
    if (process.env.NEXT_PUBLIC_USE_MOCKS !== '1') {
      // If not, redirect to a real API endpoint or show an error
      // For now, we'll just show an empty state
      console.warn('NEXT_PUBLIC_USE_MOCKS is not set to 1. Demo mode is disabled.');
      setExports([]);
      setIsLoading(false);
      return;
    }

    // Simulate API call delay
    const timer = setTimeout(() => {
      const data = getMockExports();
      setExports(data);
      setIsLoading(false);
    }, 500);

    return () => clearTimeout(timer);
  }, []);

  if (isLoading) {
    return <div className="p-4">Loading reports...</div>;
  }

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-2xl font-bold mb-6">Reports</h1>
      {exports.length === 0 ? (
        <p>No reports available yet. Complete an export from the findings page to see it here.</p>
      ) : (
        <div className="space-y-4">
          {exports.map((exp) => (
            <div key={exp.id} className="border p-4 rounded">
              <h2 className="text-xl font-semibold">{exp.fileName}</h2>
              <p>Exported on: {new Date(exp.exportedAt).toLocaleString()}</p>
              <p>Options: {JSON.stringify(exp.options)}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}