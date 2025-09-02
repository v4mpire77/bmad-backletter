'use client';

import { useEffect, useState } from 'react';
import FindingsTable from '@/components/FindingsTable';
import EvidenceDrawer from '@/components/EvidenceDrawer';

type Finding = {
  id: string;
  rule_id: string;
  detector: string;
  verdict: 'missing' | 'weak' | 'present' | 'strong';
  snippet: string;
  rationale: string;
  page_number?: number;
  char_start?: number;
  char_end?: number;
  context_before?: string;
  context_after?: string;
};

type Analysis = {
  id: string;
  status: string;
  contract_name: string;
  created_at: string;
  findings_count: number;
};

const MOCK_ANALYSIS: Analysis = {
  id: '123',
  status: 'completed',
  contract_name: 'Sample Service Agreement.pdf',
  created_at: '2025-09-02T10:30:00Z',
  findings_count: 8
};

const MOCK_FINDINGS: Finding[] = [
  {
    id: '1',
    rule_id: 'art28_data_categories',
    detector: 'Data Categories',
    verdict: 'missing',
    snippet: 'The Processor shall process personal data...',
    rationale: 'No specific data categories mentioned',
    page_number: 3,
    char_start: 245,
    char_end: 298,
    context_before: 'Service Provider responsibilities: ',
    context_after: ' in accordance with applicable law.'
  },
  {
    id: '2', 
    rule_id: 'art28_security_measures',
    detector: 'Security Measures',
    verdict: 'weak',
    snippet: 'appropriate technical measures',
    rationale: 'Vague security requirements without specifics',
    page_number: 5,
    char_start: 1024,
    char_end: 1053
  },
  {
    id: '3',
    rule_id: 'art28_subprocessors',
    detector: 'Subprocessors',
    verdict: 'present',
    snippet: 'Prior written consent required for subprocessors',
    rationale: 'Clear subprocessor approval process',
    page_number: 7,
    char_start: 1456,
    char_end: 1503
  },
  {
    id: '4',
    rule_id: 'art28_data_return',
    detector: 'Data Return/Deletion',
    verdict: 'missing',
    snippet: 'Upon termination of services...',
    rationale: 'No clear data return or deletion requirements',
    page_number: 12,
    char_start: 2847,
    char_end: 2877
  },
  {
    id: '5',
    rule_id: 'art28_audit_rights',
    detector: 'Audit Rights',
    verdict: 'weak',
    snippet: 'reasonable audit provisions',
    rationale: 'Audit rights mentioned but not detailed',
    page_number: 9,
    char_start: 2145,
    char_end: 2174
  },
  {
    id: '6',
    rule_id: 'art28_breach_notification',
    detector: 'Breach Notification',
    verdict: 'strong',
    snippet: 'Processor shall notify Controller within 24 hours of becoming aware of any personal data breach',
    rationale: 'Clear breach notification timeline and process',
    page_number: 6,
    char_start: 1598,
    char_end: 1693
  },
  {
    id: '7',
    rule_id: 'art28_processing_instructions',
    detector: 'Processing Instructions',
    verdict: 'present',
    snippet: 'process personal data only on documented instructions from Controller',
    rationale: 'Clear instruction-based processing requirement',
    page_number: 4,
    char_start: 756,
    char_end: 825
  },
  {
    id: '8',
    rule_id: 'art28_data_subject_rights',
    detector: 'Data Subject Rights',
    verdict: 'weak',
    snippet: 'assist with data subject requests',
    rationale: 'Assistance mentioned but no specific procedures',
    page_number: 8,
    char_start: 1895,
    char_end: 1930
  }
];

export default function AnalysisFindingsPage({ params }: { params: { jobId: string } }) {
  const [analysis, setAnalysis] = useState<Analysis | null>(null);
  const [findings, setFindings] = useState<Finding[]>([]);
  const [selectedFinding, setSelectedFinding] = useState<Finding | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const useMocks = process.env.NEXT_PUBLIC_USE_MOCKS === '1';

  useEffect(() => {
    async function fetchData() {
      setLoading(true);
      setError(null);

      try {
        if (useMocks) {
          // Simulate API delay
          await new Promise(resolve => setTimeout(resolve, 500));
          setAnalysis(MOCK_ANALYSIS);
          setFindings(MOCK_FINDINGS);
        } else {
          // Fetch analysis metadata
          const analysisRes = await fetch(`/api/analyses/${params.jobId}`);
          if (!analysisRes.ok) throw new Error('Failed to fetch analysis');
          const analysisData = await analysisRes.json();
          setAnalysis(analysisData);

          // Fetch findings
          const findingsRes = await fetch(`/api/analyses/${params.jobId}/findings`);
          if (!findingsRes.ok) throw new Error('Failed to fetch findings');
          const findingsData = await findingsRes.json();
          setFindings(findingsData);
        }
      } catch (err) {
        setError(err instanceof Error ? err.message : 'An error occurred');
        console.error('Error fetching data:', err);
      } finally {
        setLoading(false);
      }
    }

    fetchData();
  }, [params.jobId, useMocks]);

  const handleFindingClick = (finding: Finding) => {
    setSelectedFinding(finding);
  };

  const handleDrawerClose = () => {
    setSelectedFinding(null);
  };

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse">
          <div className="h-8 bg-gray-200 rounded w-1/3 mb-4"></div>
          <div className="h-4 bg-gray-200 rounded w-1/2 mb-6"></div>
          <div className="space-y-3">
            {[...Array(5)].map((_, i) => (
              <div key={i} className="h-16 bg-gray-200 rounded"></div>
            ))}
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-6">
        <div className="bg-red-50 border border-red-200 rounded-lg p-4">
          <h2 className="text-lg font-semibold text-red-800 mb-2">Error Loading Analysis</h2>
          <p className="text-red-700">{error}</p>
          <button 
            onClick={() => window.location.reload()}
            className="mt-3 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700 transition-colors"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  if (!analysis) {
    return (
      <div className="p-6">
        <div className="text-center py-12">
          <h2 className="text-xl font-semibold text-gray-600">Analysis not found</h2>
        </div>
      </div>
    );
  }

  return (
    <div className="p-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Analysis Results
        </h1>
        <div className="text-sm text-gray-600 space-y-1">
          <p><span className="font-medium">Contract:</span> {analysis.contract_name}</p>
          <p><span className="font-medium">Status:</span> <span className="capitalize">{analysis.status}</span></p>
          <p><span className="font-medium">Analyzed:</span> {new Date(analysis.created_at).toLocaleString()}</p>
          <p><span className="font-medium">Total Findings:</span> {analysis.findings_count}</p>
          {useMocks && (
            <p className="text-amber-600 font-medium">📋 Using mock data for development</p>
          )}
        </div>
      </div>

      {/* Findings Table */}
      <FindingsTable 
        findings={findings}
        onFindingClick={handleFindingClick}
      />

      {/* Evidence Drawer */}
      {selectedFinding && (
        <EvidenceDrawer
          finding={selectedFinding}
          onClose={handleDrawerClose}
        />
      )}
    </div>
  );
}
