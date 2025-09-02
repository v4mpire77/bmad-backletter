import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import FindingsTable from './FindingsTable';
import type { Finding } from '@bmad/shared/types';

describe('FindingsTable', () => {
  const findings: Finding[] = [
    {
      id: '1',
      doc_id: 'd1',
      rule_id: 'art28-3-a',
      verdict: 'pass',
      snippet: 'sample snippet',
      location: { page: 1, start_char: 0, end_char: 6 },
    },
  ];

  it('renders findings and opens drawer on row click', () => {
    render(<FindingsTable findings={findings} />);
    fireEvent.click(screen.getByText('art28-3-a'));
    expect(screen.getByText('Copy')).toBeInTheDocument();
  });
});
