import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import { vi } from 'vitest';
import AnalysesPage from './page';

const originalFetch = global.fetch;

afterEach(() => {
  vi.restoreAllMocks();
  global.fetch = originalFetch;
});

describe('AnalysesPage', () => {
  it('renders items fetched from the API', async () => {
    const mockItems = [
      { id: '1', name: 'Analysis One', status: 'complete' },
      { id: '2', name: 'Analysis Two', status: 'pending' },
    ];
    global.fetch = vi
      .fn()
      .mockResolvedValue({ ok: true, json: async () => mockItems }) as any;

    const page = await AnalysesPage();
    render(page);

    expect(screen.getByText('Analysis One')).toBeInTheDocument();
    expect(screen.getByText(/complete/i)).toBeInTheDocument();
    expect(screen.getByText('Analysis Two')).toBeInTheDocument();
    expect(screen.getByText(/pending/i)).toBeInTheDocument();
  });
});
