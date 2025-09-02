import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import { vi, Mock } from 'vitest';
import AnalysisDetailPage from './page';
import type { Finding } from '@/types';

vi.mock('@/lib/useJobStatus');
import useJobStatus from '@/lib/useJobStatus';

describe('AnalysisDetailPage', () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  it('shows progress while job is running', () => {
    (useJobStatus as unknown as Mock).mockReturnValue({
      status: 'queued',
      findings: null,
      error: null,
    });

    render(<AnalysisDetailPage params={{ id: '1' }} />);
    expect(screen.getByText(/Status: Queued/i)).toBeInTheDocument();
  });

  it('renders findings when job complete', () => {
    const findings: Finding[] = [
      {
        id: 'f1',
        doc_id: 'd1',
        rule_id: 'art28-3-a',
        verdict: 'pass',
        snippet: 'sample snippet',
        location: { page: 1, start_char: 0, end_char: 6 },
      },
    ];

    (useJobStatus as unknown as Mock).mockReturnValue({
      status: 'done',
      findings,
      error: null,
    });

    render(<AnalysisDetailPage params={{ id: '1' }} />);
    expect(screen.getByText('art28-3-a')).toBeInTheDocument();
  });
});
