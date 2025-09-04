import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import '@testing-library/jest-dom/vitest';
import FindingsTable from './FindingsTable';
import type { PageFinding } from '@/lib/types';
import { ensurePageFindingIds } from '@/lib/types';
import { vi } from 'vitest';

describe('FindingsTable', () => {
  const baseFindings: PageFinding[] = [
    { id: '1', rule_id: 'art28-3-a', snippet: 'sample snippet', anchors: [] },
    { rule_id: 'art28-3-b', snippet: 'second snippet', anchors: [] },
  ];

  it('renders findings and triggers callback on row click', () => {
    const findings = ensurePageFindingIds(baseFindings);
    const onRowClick = vi.fn();
    render(<FindingsTable findings={findings} onRowClick={onRowClick} />);
    fireEvent.click(screen.getByText('art28-3-a'));
    fireEvent.click(screen.getByText('art28-3-b'));
    expect(onRowClick).toHaveBeenNthCalledWith(1, findings[0]);
    expect(onRowClick).toHaveBeenNthCalledWith(2, findings[1]);
  });

  it('ensures ids are generated when missing', () => {
    const findings = ensurePageFindingIds(baseFindings);
    expect(findings[0].id).toBe('1');
    expect(findings[1].id).toBeDefined();
  });
});
