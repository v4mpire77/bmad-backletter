import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import FindingsTable from './FindingsTable';
import type { PageFinding } from '@/lib/types';

describe('FindingsTable', () => {
  const findings: PageFinding[] = [
    {
      id: '1',
      rule_id: 'art28-3-a',
      snippet: 'sample snippet',
      anchors: [],
    },
  ];

  it('renders findings and opens drawer on row click', () => {
    render(<FindingsTable findings={findings} />);
    fireEvent.click(screen.getByText('art28-3-a'));
    expect(screen.getByText('Copy')).toBeInTheDocument();
  });
});
