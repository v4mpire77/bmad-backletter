import type { PageFinding } from '@/lib/types';

export interface ReportMeta {
  id: number;
  createdAt: string;
}

export const mockReports: ReportMeta[] = [];

export function addReport() {
  mockReports.push({
    id: mockReports.length + 1,
    createdAt: new Date().toISOString(),
  });
}

export function getReports() {
  return mockReports;
}

// Mock analysis data
export const mockAnalysis = {
  findings: [
    {
      id: '1',
      rule_id: 'art28_data_categories',
      snippet: 'The Processor shall process personal data...',
      evidence: [{ page: 3, start: 245, end: 298 }],
      anchors: ['personal data', 'process']
    },
    {
      id: '2', 
      rule_id: 'art28_security_measures',
      snippet: 'appropriate technical measures',
      evidence: [{ page: 5, start: 1024, end: 1053 }],
      anchors: ['technical measures']
    },
    {
      id: '3',
      rule_id: 'art28_subprocessors',
      snippet: 'Prior written consent required for subprocessors',
      evidence: [{ page: 7, start: 1456, end: 1503 }],
      anchors: ['written consent', 'subprocessors']
    }
  ] as PageFinding[]
};
