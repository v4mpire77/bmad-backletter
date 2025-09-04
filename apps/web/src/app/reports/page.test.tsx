import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import ReportsPage from './page';
import { mockReports } from '../../lib/mockReports';

describe('ReportsPage', () => {
  beforeEach(() => {
    mockReports.length = 0;
  });

  it('renders stub text when no reports exist', () => {
    render(<ReportsPage />);
    expect(screen.getByText(/Report history will appear here/i)).toBeInTheDocument();
  });

  it('lists stored reports', () => {
    mockReports.push({ id: 1, createdAt: '2024-01-01T00:00:00Z' });
    render(<ReportsPage />);
    expect(screen.getByText('Report 1')).toBeInTheDocument();
  });
});
