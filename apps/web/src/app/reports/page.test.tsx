import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import ReportsPage from './page';

describe('ReportsPage', () => {
  it('renders stub text', () => {
    render(<ReportsPage />);
    expect(screen.getByText(/Report history will appear here/i)).toBeInTheDocument();
  });
});
