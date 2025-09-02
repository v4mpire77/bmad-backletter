'use client';

import { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useSearchParams } from 'next/navigation';
import FindingsClient from '@/components/FindingsClient';
import { mockFindingsData } from '@/lib/mocks';
import { Finding } from '@/lib/types';

// This is a mock function to simulate fetching data based on id
// In a real application, this would be an API call
const fetchFindingsData = (id: string): Finding[] => {
  // For demo purposes, we only have mock-1
  if (id === 'mock-1') {
    return mockFindingsData;
  }
  return [];
};

export default function AnalysisPage({ params }: { params: { id: string } }) {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [findings, setFindings] = useState<Finding[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check if mocks are enabled
    if (process.env.NEXT_PUBLIC_USE_MOCKS !== '1') {
      // If not, redirect to a real API endpoint or show an error
      // For now, we'll just show an empty state
      console.warn('NEXT_PUBLIC_USE_MOCKS is not set to 1. Demo mode is disabled.');
      setFindings([]);
      setIsLoading(false);
      return;
    }

    // Simulate API call delay
    const timer = setTimeout(() => {
      const data = fetchFindingsData(params.id);
      setFindings(data);
      setIsLoading(false);
    }, 500);

    return () => clearTimeout(timer);
  }, [params.id]);

  if (isLoading) {
    return <div className="p-4">Loading findings...</div>;
  }

  return (
    <div className="container mx-auto py-8">
      <h1 className="text-2xl font-bold mb-6">Analysis for {params.id}</h1>
      <FindingsClient findings={findings} />
    </div>
  );
}