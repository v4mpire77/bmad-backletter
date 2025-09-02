import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import AnalysesPage from './page';

describe('AnalysesPage', () => {
  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('renders analyses returned from API', async () => {
    const analyses = [
      { id: '1', name: 'Report A', status: 'pending' },
      { id: '2', name: 'Report B', status: 'complete' },
    ];

    vi.spyOn(global, 'fetch').mockResolvedValue({
      ok: true,
      json: async () => analyses,
    } as any);

    render(<AnalysesPage />);

    expect(await screen.findByText('Report A')).toBeInTheDocument();
    expect(screen.getByText('Report B')).toBeInTheDocument();
  });

  it('shows empty state when no analyses returned', async () => {
    vi.spyOn(global, 'fetch').mockResolvedValue({
      ok: true,
      json: async () => [],
    } as any);

    render(<AnalysesPage />);

    expect(
      await screen.findByText(/No analyses yet\./i),
    ).toBeInTheDocument();
  });
});

